import logging
import paramiko

from variables import FAKE_USERNAME, FAKE_PASSWORD

class FakeSSHServer(paramiko.ServerInterface):
    def check_auth_password(self, username, password):
        logging.info(f"Authentication attempt: username={username}, password={password}")

        if (username == FAKE_USERNAME) and (password == FAKE_PASSWORD):
            logging.info("Authentication successful")
            return paramiko.AUTH_SUCCESSFUL

        logging.info("Authentication failed")
        return paramiko.AUTH_FAILED

    def check_auth_publickey(self, username, key):
        return paramiko.AUTH_FAILED

    def check_channel_request(self, kind, chanid):
        logging.info(f"Channel request: kind={kind}, id={chanid}")
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        logging.info(f"PTY request: term={term}, size={width}x{height}")
        return True

    def check_channel_shell_request(self, channel):
        logging.info("Shell request granted")
        return True

    def check_channel_exec_request(self, channel, command):
        logging.info(f"Exec request: {command}")
        return True