#!/usr/bin/env python3

import re
import sys
import requests
from typing import Tuple, List


def usage():
    """Usage:
    {} <WORD_EN|WORD_ZH>...
    """


def is_en_word(keyword: str) -> bool:
    """

    :param keyword:
    :return:
    """
    for letter in keyword:
        if letter < 'A' or letter > 'z':
            return False
    return True


def search_zh_word(keyword: str) -> List[str]:
    """

    :param keyword:
    :return:
    """
    url = 'https://dict.youdao.com/w/{}/#keyfrom=dict2'.format(keyword)
    headers = {
        'Host': 'dict.youdao.com',
        'Referer': 'https://dict.youdao.com/?keyfrom=cidian',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    html = response.text
    part = '<span class="contentTitle"><a class="search-js" href="/w/(.+?)/#keyfrom=E2Ctranslation">'
    return re.compile(part).findall(html)


def search_en_word(keyword: str) -> Tuple[str, str, str]:
    """

    :param keyword:
    :return:
    """
    uk_phonetic, us_phonetic = '', ''
    url = 'https://dict.youdao.com/w/eng/{}/#keyfrom=dict2'.format(keyword)
    headers = {
        'Host': 'dict.youdao.com',
        'Referer': 'https://dict.youdao.com/?keyfrom=cidian',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    html = response.text
    part = '<span class="phonetic">(.+?)</span>'
    phonetics = re.compile(part).findall(html)
    if len(phonetics) >= 1:
        uk_phonetic = phonetics[0]
    if len(phonetics) >= 2:
        us_phonetic = phonetics[1]
    return uk_phonetic, us_phonetic, url


def column_widths(rows: List[List[str]]) -> List[int]:
    """

    :param rows:
    :return:
    """
    widths = []
    for row in rows:
        idx = 0
        for item in row:
            if idx + 1 > len(widths):
                widths.append(0)
            if len(item) > widths[idx]:
                widths[idx] = len(item)
            idx += 1
    return widths


def rows_to_md_table(rows: List[List[str]]) -> List[str]:
    """

    :param rows:
    :return:
    """
    table = []
    widths = column_widths(rows)

    # generate dividing line
    line = '|'
    for width in widths:
        line += ('-{:-<' + str(width) + '}-|').format('')
    table.append(line)

    # generate contents
    for row in rows:
        line = '|'
        idx = 0
        for item in row:
            if idx:
                line += (' {:<' + str(widths[idx]) + '} |').format(item)
            else:
                line += (' {:>' + str(widths[idx]) + '} |').format(item)
            idx += 1
        table.append(line)

    table[0], table[1] = table[1], table[0]
    return table


def print_as_md_table(rows: List[List[str]]):
    print('')
    for line in rows_to_md_table(rows):
        print(line)
    print('')


def main():
    if len(sys.argv) == 1:
        print(usage.__doc__.format(sys.argv[0]))
        sys.exit(0)

    data = [['', 'KEYWORD', 'UK PHONETIC', 'US PHONETIC', 'URL']]

    cnt = 0
    for word in sys.argv[1:]:
        cnt += 1
        if is_en_word(word):
            data.append([str(cnt), word, *search_en_word(word)])
        else:
            for en_word in search_zh_word(word):
                data.append([str(cnt), en_word, *search_en_word(en_word)])

    print_as_md_table(data)


if __name__ == "__main__":
    main()
