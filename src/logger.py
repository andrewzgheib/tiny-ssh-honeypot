import logging
import os
import platform
import socket
import sys

def configure_logging():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
    log_path = os.path.join(parent_dir, 'honeypot.log')

    logging.basicConfig(
        filename=log_path,
        format='%(asctime)s [%(levelname)s]:  %(message)s',
        datefmt='%d-%m-%Y %H:%M:%S',
        level=logging.INFO
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s', '%d-%m-%Y %H:%M:%S'))
    logging.getLogger().addHandler(console_handler)

    logging.info('Honeypot logger initialized.')
    logging.info(f"System: {platform.system()} {platform.release()} ({platform.architecture()[0]})")
    logging.info(f"Hostname: {socket.gethostname()}")