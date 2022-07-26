import csv
import os
import re
import sys
import string

import path
import requests

import youdao


def get_ielts_words_by_prefix(prefix: str) -> list[list[str]]:
    words = []
    idx = {'a': 785911, 'b': 785912, 'c': 785913, 'd': 785914, 'e': 785915,
           'f': 785917, 'g': 785918, 'h': 785920, 'i': 785921, 'j': 785922,
           'k': 785923, 'l': 785924, 'm': 785925, 'n': 785926, 'o': 785927,
           'p': 785929, 'q': 785931, 'r': 785944, 's': 785945, 't': 785946,
           'u': 785947, 'v': 785948, 'w': 785950, 'x': 785951, 'y': 785952, 'z': 785953}[prefix]
    urls = ['https://ielts.koolearn.com/{date}/{idx}.html'.format(date='20140411', idx=idx)]
    headers = {
        'Host': 'ielts.koolearn.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    try:
        response = requests.get(urls[0], headers=headers)
        tmp_results = re.compile('<div class="pgbar pg" id="page">(.+?)</div>').findall(response.text.replace('\n', ''))
        urls.extend(re.compile('<a target="_self" href="(.+?)">').findall(tmp_results[0]))
    except ConnectionError as e:
        print(e)

    for url in urls:
        try:
            response = requests.get(url, headers=headers)
            response.encoding = 'utf-8'
            tmp_results = re.compile('<div class="xqy_core_text">(.+?)</div>').findall(response.text.replace('\n', ''))
            words[:0] = re.compile('<p>\u3000\u3000(.+?)</p>').findall(tmp_results[0])
        except ConnectionError as e:
            print(e)

    words.sort()
    rows = []
    for word in words:
        if ' ' in word:
            en = word.split(' ')[0]
            zh = word.replace(en + ' ', '')
        else:
            en = re.compile('([A-Za-z.]+)').findall(word)[0]
            zh = word.replace(en, '')
        rows.append([en, zh])
    return rows


def main():
    input_file, output_file = 'ielts_words.csv', 'ielts_words.tmp.csv'

    rows = []
    exist_words = set()
    if os.path.exists(input_file):
        with open(input_file) as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                rows.append(row)
                if all(v for v in row):  # check if list contains empty item
                    exist_words.add(row[0])
    else:
        rows = []
        # rows = [['WORD', 'UK PRONUNCIATION', 'US PRONUNCIATION', 'URL', 'TRANSLATE']]

    with open(output_file, 'w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(rows)
        for letter in [string.ascii_lowercase[i:i + 1] for i in range(0, 26, 1)]:
            words = get_ielts_words_by_prefix(letter)
            for en_zh in words:
                en, zh = en_zh[0], en_zh[1]
                if en not in exist_words:
                    uk, us, url = youdao.search_en_word(en)
                    row = [en, uk, us, url, zh]
                    print(row)  # for debug
                    rows.append(row)
                    writer.writerow(row)

    os.system('cat ielts_words.tmp.csv | LC_COLLATE=C sort --ignore-case | uniq >ielts_words.csv')


if __name__ == '__main__':
    main()
