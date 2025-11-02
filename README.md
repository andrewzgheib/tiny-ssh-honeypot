# Tiny SSH Honeypot

A tiny SSH honeypot built with [Paramiko](https://www.paramiko.org/). This honeypot logs credentials and commands to analyze attacker behavior and returns fake responses safely without executing anything.

## Features

- Password auth with pre-determined fake credentials
- Interactive shell simulation with a realistic prompt
- Canned responses for common commands
- Console + file logging

## Install

```bash
git clone https://github.com/andrewzgheib/tiny-ssh-honeypot.git
cd tiny-ssh-honeypot
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Connect using an SSH client to the honeypot server (default port 2222) with the fake credentials defined in [variables.py](https://github.com/andrewzgheib/tiny-ssh-honeypot/blob/main/src/variables.py).

## Configuration

Edit [variables.py](https://github.com/andrewzgheib/tiny-ssh-honeypot/blob/main/src/variables.py) to customize the honeypot's behavior:

- `HOST`: The hostname or IP address to bind the honeypot server.
- `PORT`: The port to listen on.
- `MAX_CONNECTIONS`: The maximum number of concurrent connections.
- `RSA_KEY_BITS`: The size of the RSA key to generate for the SSH server.
- `FAKE_USERNAME`: The username to use for fake authentication.
- `FAKE_PASSWORD`: The password to use for fake authentication.
- `FAKE_RESPONSES`: Customize the responses for specific commands.

> [!WARNING]
> Never use this in production.
> For educational & research purposes only.
