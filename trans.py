#!/usr/bin/env python3

import sys

import youdao

if __name__ == '__main__':
    youdao.handle_args()
    youdao.search_words(*sys.argv[1:])
