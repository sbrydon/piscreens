from datetime import datetime
import socket
from nose.tools import *  # noqa
from piscreens import systeminfo


def test_get_datetime_format():
    date_str = systeminfo.get_datetime()
    assert is_valid_datetime_string(date_str, '%d %b %Y, %H:%M')


def test_get_time_format():
    date_str = systeminfo.get_time()
    assert is_valid_datetime_string(date_str, '%H:%M:%S')


def test_get_ip():
    ip = systeminfo.get_ip()
    assert is_valid_ipv4_address(ip) or is_valid_ipv6_address(ip)


def is_valid_datetime_string(date_str, expected_fmt):
    try:
        datetime.strptime(date_str, expected_fmt)
        return True
    except ValueError:
        return False


def is_valid_ipv4_address(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:
        return False

    return True


def is_valid_ipv6_address(address):
    try:
        socket.inet_pton(socket.AF_INET6, address)
    except socket.error:
        return False
    return True
