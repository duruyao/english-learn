#!/usr/bin/env python3

import os
import re
import sys
import csv
import string
import signal
import requests
import urllib.parse
from typing import List, Tuple, Dict, Union

from println import warning_ln


def app_home() -> str:
    return os.path.dirname(os.path.realpath(sys.argv[0]))


def show_usage():
    """

    :return:
    """
    usage = """Usage:
    {execute} [<WORD_EN|WORD_ZH> ...]
    """
    execute = f'python3 {sys.argv[0]}' if '.py' == sys.argv[0][-3:] else os.path.basename(sys.argv[0])
    print(usage.format(execute=execute))


def signal_handler(sig, frame):
    print()
    sys.exit(0)


def handle_args():
    """

    :return:
    """
    words = sys.argv[1:]
    signal.signal(signal.SIGINT, signal_handler)
    if '-h' in words or '--help' in words:
        show_usage()
        return
    if not words:
        print('Youdao Dictionary CLI Interactor',
              '────────────────────────────────',
              'Type the words (zh-cn, en) you want to query.',
              'Type "exit()", "quit()" or CTRL-C to exit the interactor.', sep='\n')
        while True:
            words = input('>>> ').split(' ')
            if 'exit()' in words or 'quit()' in words:
                return
            search_words(*words)
    search_words(*words)


def is_en(keyword: str) -> bool:
    """

    :param keyword:
    :return:
    """
    if keyword[0] not in string.ascii_letters:
        return False
    return True


def save_cache(data: Dict, csv_basename: str, csv_dir: str = f'{app_home()}/cache'):
    csv_filename = f'{csv_dir}/{csv_basename}'
    if not os.path.exists(csv_filename):
        os.makedirs(os.path.dirname(csv_filename), exist_ok=True)
        with open(csv_filename, 'a', newline='\n') as file:
            writer = csv.DictWriter(file, fieldnames=list(data.keys()))
            writer.writeheader()
    with open(csv_filename, 'r') as file:
        reader = csv.DictReader(file)
        for record in reader:
            if record['key'] == data['key']:
                return
    with open(csv_filename, 'a', newline='\n') as file:
        writer = csv.DictWriter(file, fieldnames=list(data.keys()))
        writer.writerow(data)


def search_zh_online(keyword: str, cache: bool = True) -> Tuple[List[str], bool]:
    """

    :param keyword:
    :param cache:
    :return:
    """
    url = 'https://dict.youdao.com/w/{}/#keyfrom=dict2'.format(urllib.parse.quote(keyword))
    headers = {
        'Host': 'dict.youdao.com',
        'Referer': 'https://dict.youdao.com/?keyfrom=cidian',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
        html = response.text
        part = '<span class="contentTitle"><a class="search-js" href="/w/(.+?)/#keyfrom=E2Ctranslation">'
        result = re.compile(part).findall(html)
        if cache and result:
            save_cache({'key': keyword, 'result': result}, csv_basename='search_zh_online.csv')
        return result if result else [''], result is not []
    except BaseException as error:
        warning_ln(f'Unexpected {error = }, {type(error) = }')
        return [''], False


def search_zh_offline(keyword: str,
                      csv_basename: str = 'search_zh_online.csv',
                      csv_dir: str = f'{app_home()}/cache') -> Tuple[List[str], bool]:
    if os.path.exists(f'{csv_dir}/{csv_basename}'):
        with open(f'{csv_dir}/{csv_basename}', 'r') as file:
            reader = csv.DictReader(file)
            for record in reader:
                if record['key'] == keyword:
                    return record['result'][2:-2].split('\', \''), True
    return [], False


def search_en_online(keyword: str, cache: bool = True) -> Tuple[Dict[str, Union[str, List[str]]], bool]:
    """

    :param keyword:
    :param cache:
    :return:
    """
    url = 'https://dict.youdao.com/w/eng/{}/#keyfrom=dict2'.format(urllib.parse.quote(keyword))
    headers = {
        'Host': 'dict.youdao.com',
        'Referer': 'https://dict.youdao.com/?keyfrom=cidian',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        html = response.text.replace('\n', '')
        symbols = re.compile('<span class="phonetic">(.+?)</span>').findall(html)
        uk, us = symbols[0] if len(symbols) > 0 else '', symbols[1] if len(symbols) > 1 else ''
        url = 'https://dict.youdao.com/result?word={}&lang=en'.format(urllib.parse.quote(keyword))
        tmp = re.compile('<div class="trans-container">(.+?)</div>').findall(html)
        trans = re.compile('<li>(.+?)</li>').findall(tmp[0]) if len(tmp) else []
        additions = re.compile('<p class="additional">\[ +(.+?) +\]</p').findall(html)
        addition = ''
        if len(additions):
            addition = additions[0]
            while '  ' in addition:
                addition = addition.replace('  ', ' ')
            addition = '[{}]'.format(addition)
        result = {'key': keyword, 'uk': uk, 'us': us, 'url': url, 'trans': trans, 'addition': addition}
        if cache and trans:
            save_cache(result, csv_basename='search_en_online.csv')
        return result, trans is not []
    except BaseException as error:
        warning_ln(f'Unexpected {error = }, {type(error) = }')
        return {'key': keyword, 'uk': '', 'us': '', 'url': '', 'trans': '', 'addition': ''}, False


def search_en_offline(keyword: str,
                      csv_basename: str = 'search_en_online.csv',
                      csv_dir: str = f'{app_home()}/cache') -> Tuple[Dict[str, Union[str, List[str]]], bool]:
    if not keyword:
        return {'key': keyword, 'uk': '', 'us': '', 'url': '', 'trans': '', 'addition': ''}, True
    if os.path.exists(f'{csv_dir}/{csv_basename}'):
        with open(f'{csv_dir}/{csv_basename}', 'r') as file:
            reader = csv.DictReader(file)
            for record in reader:
                if record['key'] == keyword:
                    record['trans'] = record['trans'][2:-2].split('\', \'')
                    return record, True
    return {}, False


def search_words(*args: str):
    """

    :param args:
    :return:
    """
    result_fmt = """\
{begin}\
│   {key}
│   {uk} {us}
│   {trans}
│   {addition}
│   {url}\
{end}"""

    for word in args:
        if is_en(word):
            (result, ok) = search_en_offline(word)
            (result, ok) = search_en_online(word) if not ok else (result, ok)
            print(result_fmt.format(key=result['key'],
                                    begin='┌──\n', end='\n└──',
                                    uk='英 ' + result['uk'] if len(result['uk']) else '',
                                    us='美 ' + result['us'] if len(result['us']) else '',
                                    trans='\n│   '.join(result['trans']),
                                    addition=result['addition'], url=result['url']))
        else:
            (en_words, ok) = search_zh_offline(word)
            (en_words, ok) = search_zh_online(word) if not ok else (en_words, ok)
            cnt = 1
            for en_word in en_words:
                (result, ok) = search_en_offline(en_word)
                (result, ok) = search_en_online(en_word) if not ok else (result, ok)
                print(result_fmt.format(key=result['key'],
                                        begin='┌──\n' if cnt == 1 else '├──\n',
                                        end='\n└──' if cnt == len(en_words) else '',
                                        uk='英 ' + result['uk'] if len(result['uk']) else '',
                                        us='美 ' + result['us'] if len(result['us']) else '',
                                        trans='\n│   '.join(result['trans']),
                                        addition=result['addition'], url=result['url']))
                cnt += 1


if __name__ == "__main__":
    handle_args()
