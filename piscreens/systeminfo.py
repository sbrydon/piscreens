import socket
from datetime import datetime


def get_datetime():
    now = datetime.now()
    return datetime.strftime(now, '%d %b %Y, %H:%M')


def get_time():
    now = datetime.now()
    return datetime.strftime(now, '%H:%M:%S')


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    return s.getsockname()[0]
