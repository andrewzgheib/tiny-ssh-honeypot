import logging
import socket
import threading

from paramiko import RSAKey, Transport, SSHException

from logger import configure_logging
from fake_ssh_server import FakeSSHServer
from variables import (
    HOST,
    PORT,
    MAX_CONNECTIONS,
    RSA_KEY_BITS,
    FAKE_RESPONSES,
    FAKE_USERNAME,
)

configure_logging()

def handle_connection(client_socket, server_key):
    transport = Transport(client_socket)
    transport.add_server_key(server_key)

    server = FakeSSHServer()
    try:
        transport.start_server(server=server)
    except SSHException as e:
        logging.error(f"SSH negotiation failed: {e}")
        return

    channel = transport.accept(20)
    if channel is None:
        logging.info("No channel opened, closing connection")
        transport.close()
        return

    logging.info("Channel opened, simulating shell")
    close_reason = "unknown"
    try:
        hostname = FAKE_RESPONSES.get('hostname', 'host')
        prompt = f"{FAKE_USERNAME}@{hostname}:~$ "

        line_buf = []
        last_was_cr = False

        channel.send(prompt)
        while True:
            data = channel.recv(1024)
            if not data:
                close_reason = "client disconnected"
                break

            for b in data:
                if b in (10, 13):  # \n or \r
                    if b == 10 and last_was_cr:
                        last_was_cr = False
                        continue

                    channel.send("\r\n")

                    command = ''.join(line_buf).strip()
                    line_buf.clear()

                    if command:
                        logging.info(f"Attacker sent: {command}")

                        if command.lower() in ("exit", "quit", "logout"):
                            channel.send("logout\r\n")
                            close_reason = "exit command"
                            raise StopIteration

                        response = FAKE_RESPONSES.get(command)
                        if response is None:
                            base = command.split()[0]
                            response = FAKE_RESPONSES.get(base)

                        if response is None:
                            channel.send(f"bash: {command}: command not found\r\n")
                        else:
                            if not response.endswith("\n") and not response.endswith("\r\n"):
                                channel.send(response + "\r\n")
                            else:
                                channel.send(response.replace("\n", "\r\n"))

                    channel.send(prompt)
                    last_was_cr = (b == 13)
                    continue

                # Handle backspace (BS=0x08 or DEL=0x7f)
                if b in (8, 127):
                    if line_buf:
                        line_buf.pop()
                        channel.send("\b \b")
                    continue

                # Handle Ctrl-C (ETX)
                if b == 3:
                    line_buf.clear()
                    channel.send("^C\r\n" + prompt)
                    continue

                # Ignore escape sequences (arrows, etc.) by swallowing ESC (27)
                if b == 27:
                    # TODO: VT100 editing
                    continue

                if 32 <= b <= 126 or b == 9:
                    ch = chr(b)
                    line_buf.append(ch)
                    channel.send(ch)
                    continue

                last_was_cr = (b == 13)
    except Exception as e:
        if isinstance(e, StopIteration):
            pass
        else:
            close_reason = f"error: {e}"
            logging.error(f"Error on channel: {e}")
    finally:
        try:
            peer = client_socket.getpeername()
            peer_str = f"{peer[0]}:{peer[1]}"
        except Exception:
            peer_str = "unknown"
        logging.info(f"Connection closed from {peer_str} ({close_reason})")
        channel.close()
        transport.close()

def main():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(MAX_CONNECTIONS)

    logging.info(f"Honeypot listening on {HOST}:{PORT}")

    server_key = RSAKey.generate(RSA_KEY_BITS)

    while True:
        client_socket, client_address = server_socket.accept()
        logging.info(f"Attacker connected from {client_address[0]}:{client_address[1]}")
        t = threading.Thread(target=handle_connection, args=(client_socket, server_key), daemon=True)
        t.start()

if __name__ == "__main__":
    main()