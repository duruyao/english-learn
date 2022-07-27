#!/usr/bin/env python3

import re
import sys
import string
import requests
import urllib.parse


def usage():
    """Usage:
    python3 {script} <WORD_EN|WORD_ZH>...
    """


def is_en_word(keyword: str) -> bool:
    """

    :param keyword:
    :return:
    """
    if keyword[0] not in string.ascii_letters:
        return False
    return True


def search_zh_word(keyword: str) -> list[str]:
    """

    :param keyword:
    :return:
    """
    url = 'https://dict.youdao.com/w/{}/#keyfrom=dict2'.format(urllib.parse.quote(keyword))
    headers = {
        'Host': 'dict.youdao.com',
        'Referer': 'https://dict.youdao.com/?keyfrom=cidian',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    result = []
    try:
        response = requests.get(url, headers=headers)
        html = response.text
        part = '<span class="contentTitle"><a class="search-js" href="/w/(.+?)/#keyfrom=E2Ctranslation">'
        result = re.compile(part).findall(html)
    except ConnectionError as e:
        print(e)
    return result


def search_en_word(keyword: str) -> dict:
    """

    :param keyword:
    :return:
    """
    uk_symbol, us_symbol = '', ''
    trans = []
    url = 'https://dict.youdao.com/w/eng/{}/#keyfrom=dict2'.format(urllib.parse.quote(keyword))
    headers = {
        'Host': 'dict.youdao.com',
        'Referer': 'https://dict.youdao.com/?keyfrom=cidian',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        symbols = re.compile('<span class="phonetic">(.+?)</span>').findall(response.text.replace('\n', ''))
        uk_symbol, us_symbol = symbols[0] if len(symbols) > 0 else '', symbols[1] if len(symbols) > 1 else ''
        tmp = re.compile('<div class="trans-container">(.+?)</div>').findall(response.text.replace('\n', ''))
        trans = re.compile('<li>(.+?)</li>').findall(tmp[0].replace('\n', ''))
    except (ConnectionError, ValueError, IndexError) as e:
        print(e)
    return {'key': keyword, 'uk': uk_symbol, 'us': us_symbol, 'url': url, 'trans': trans}


def column_widths(rows: list[list[str]]) -> list[int]:
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


def rows_to_md_table(rows: list[list[str]]) -> list[str]:
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


def print_md_table(rows: list[list[str]]):
    for line in rows_to_md_table(rows):
        print(line)


def write_md_table(rows: list[list[str]], filename: str):
    with open(filename, 'w') as file:
        for line in rows_to_md_table(rows):
            file.write(line + '\n')


result_fmt = """{begin}
{sep}{key}
{sep}英 {uk}{sep}美 {us}
{sep}{trans}
{sep}{url}
{end}
"""


def main():
    if len(sys.argv) == 1:
        print(usage.__doc__.format(script=sys.argv[0]))
        sys.exit(0)

    for word in sys.argv[1:]:
        if is_en_word(word):
            result = search_en_word(word)
            print(result_fmt.format(begin='{', end='}', sep='\t',
                                    key=result['key'], url=result['url'],
                                    uk=result['uk'], us=result['us'],
                                    trans='\n\t'.join(result['trans'])))
        else:
            for en_word in search_zh_word(word):
                result = search_en_word(en_word)
                print(result_fmt.format(begin='{', end='}', sep='\t',
                                        key=result['key'], url=result['url'],
                                        uk=result['uk'], us=result['us'],
                                        trans='\n\t'.join(result['trans'])))


if __name__ == "__main__":
    main()
