#!/usr/bin/env python3

import os
import sys
import time
import random
import string
import getopt
import pathlib
import datetime


# date:   2022-07-08
# author: duruyao@gmail.com
# desc:   command line game for typing practice


def info_ln(values):
    print('\033[1;32;32m', values, '\033[m', sep='', end='\n')


def trace_ln(values):
    print('\033[1;32;34m', values, '\033[m', sep='', end='\n')


def warning_ln(values):
    print('\033[1;32;33m', values, '\033[m', sep='', end='\n')


def error_ln(values):
    print('\033[1;32;31m', values, '\033[m', sep='', end='\n')


def show_usage():
    """Usage: python3 {script} [OPTIONS]

Command line game for typing practice

Options:
  -b, --batch=<N>                   Set batch size (default: 100)
  -d, --diff=<easy|normal|hard>     Select game difficulty (default: easy)
  -l, --length=<N>                  Set length of random string (default: 1)
  -h, --help                        Display this help message

Examples:
  python3 {script}
  python3 {script} -l 1 -b 100 -d easy
  python3 {script} --length=1 --batch=100 --diff=easy
    """
    script = os.path.realpath(sys.argv[0])
    print(show_usage.__doc__.format(script=script))


def rand_str(chars=string.ascii_lowercase + ',./;', length=10, sep=''):
    return sep.join(random.choice(chars) for _ in range(length))


def main():
    diff = 'easy'
    length = 1
    batch = 100
    thesaurus = {'easy': string.ascii_lowercase + ',./;',
                 'normal': string.ascii_letters + string.digits + ',./;',
                 'hard': string.printable}

    try:
        opts, args = getopt.getopt(sys.argv[1:], "b:d:l:h", ["batch=", "diff=", "length=", "help"])
    except getopt.GetoptError as e:
        error_ln(e)
        show_usage()
        sys.exit(1)

    for opt_key, opt_value in opts:
        if opt_key in ('-b', '--batch'):
            batch = int(opt_value)
        elif opt_key in ('-d', '--diff'):
            diff = str(opt_value)
        elif opt_key in ('-l', '--length'):
            length = int(opt_value)
        elif opt_key in ('-h', '--help'):
            show_usage()
            sys.exit(0)

    level = '{}-{}-{}'.format(diff, length, batch)
    history_dir = '{}/.qwer'.format(os.path.expanduser('~'))
    history_file = '{}/{}.md'.format(history_dir, level)

    pathlib.Path(history_dir).mkdir(parents=True, exist_ok=True)
    if not os.path.exists(history_file):
        with open(history_file, 'w') as file:
            file.write('| SCORE  | LEVEL          | DATE                | GAMER            |\n')
            file.write('|--------|----------------|---------------------|------------------|\n')

    gain = 0
    loss = 0
    gamer = 'someone'

    for i in 3, 2, 1, 'Go':
        print('{:<2}!'.format(i), sep='')
        time.sleep(1)
    print()

    for i in range(batch):
        print('[{:>3}]'.format(i + 1))
        word = rand_str(chars=thesaurus[diff], length=length)
        answer = ''
        begin = datetime.datetime.now()
        while answer != word:
            print('      Q: ', end='')
            trace_ln(word)
            print('      A: ', end='')
            answer = input()
        end = datetime.datetime.now()
        duration = end - begin
        print('      T: ', end='')
        if duration.total_seconds() < length + 1:
            info_ln(duration)
            gain += 1
        else:
            warning_ln(duration)
            loss += 1
    score = '%.2f' % ((gain * 100) / (gain + loss))

    print()
    now = datetime.datetime.now()
    date = '{:>4}-{:0>2}-{:0>2} {:0>2}:{:0>2}:{:0>2}'. \
        format(now.year, now.month, now.day, now.hour, now.minute, now.second)
    print('SCORE: %s' % score)
    print('YOUR NAME: ', end='')
    name = input()
    if len(name):
        gamer = name[:16]
    print('HISTORY: ')

    with open(history_file, 'r') as file:
        lines = file.readlines()
    lines.append('| {:0>6} | {:<14} | {:<19} | {:<16} | <-\n'.format(score, level, date, gamer))

    for line in lines[:2]:
        print('        ' + line, end='')
    lines[:] = lines[2:]
    lines.sort(reverse=True)
    for line in lines:
        print('        ' + line, end='')

    with open(history_file, 'a') as file:
        file.write('| {:0>6} | {:<14} | {:<19} | {:<16} |\n'.format(score, level, date, gamer))


if __name__ == '__main__':
    main()
