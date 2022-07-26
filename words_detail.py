import re
import string
import sys

import requests


def get_words_by_length(*lens: int) -> list[str]:
    words = []
    for length in set(lens):
        length = min(max(length, 1), 20)
        if length == 1:
            words[:0] = [string.ascii_lowercase[i:i + length] for i in range(0, 26, length)]
        else:
            url = 'https://www.wordsdetail.com/{len}-letter-words/'.format(len=length)
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
            try:
                response = requests.get(url, headers=headers)
                html = response.text
                part = '<li class="item">([a-z].+?)</li>'
                words[:0] = re.compile(part).findall(html)
            except ConnectionError as e:
                print('URL: {} ERROR: {}'.format(url, e))

    return words


if __name__ == '__main__':
    print(get_words_by_length(*map(int, sys.argv[1:])))
