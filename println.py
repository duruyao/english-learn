import sys
from typing import Any


def fatal_ln(*args: Any, sep: str = ' ', end: str = '\n'):
    """

    :param args:
    :param sep:
    :param end:
    :return:
    """
    print('\033[1;32;31m', sep.join([str(x) for x in args]), '\033[m', sep='', end=end)
    sys.exit(1)


def error_ln(*args: Any, sep: str = ' ', end: str = '\n'):
    """

    :param args:
    :param sep:
    :param end:
    :return:
    """
    print('\033[0;32;31m', sep.join([str(x) for x in args]), '\033[m', sep='', end=end)


def warning_ln(*args: Any, sep: str = ' ', end: str = '\n'):
    """

    :param args:
    :param sep:
    :param end:
    :return:
    """
    print('\033[0;32;33m', sep.join([str(x) for x in args]), '\033[m', sep='', end=end)


def trace_ln(*args: Any, sep: str = ' ', end: str = '\n'):
    """

    :param args:
    :param sep:
    :param end:
    :return:
    """
    print('\033[0;32;36m', sep.join([str(x) for x in args]), '\033[m', sep='', end=end)


def info_ln(*args: Any, sep: str = ' ', end: str = '\n'):
    """

    :param args:
    :param sep:
    :param end:
    :return:
    """
    print('\033[0;32;32m', sep.join([str(x) for x in args]), '\033[m', sep='', end=end)


def debug_ln(*args: Any, sep: str = ' ', end: str = '\n'):
    """

    :param args:
    :param sep:
    :param end:
    :return:
    """
    print('\033[0;32;34m', sep.join([str(x) for x in args]), '\033[m', sep='', end=end)
