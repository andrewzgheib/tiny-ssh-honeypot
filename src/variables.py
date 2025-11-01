HOST = '127.0.0.1'
PORT = 2222
MAX_CONNECTIONS = 5

RSA_KEY_BITS = 2048

FAKE_USERNAME = "admin"
FAKE_PASSWORD = "12345"

# TODO: Add support for more commands
FAKE_RESPONSES = {
    'pwd': '/home/admin',
    'whoami': 'admin',
    'hostname': 'ubuntu-server',
    'uname': 'Linux',
    'users': 'admin',
    'id': 'uid=1000(admin) gid=1000(admin) groups=1000(admin),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),101(lxd)',
    'tty': '/dev/pts/0',
    'umask': '0002',
}