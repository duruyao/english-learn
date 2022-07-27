#!/usr/bin/env python3

import os
import sys
import csv
import youdao


def usage():
    """Usage:
    python3 {script} <IN_CSV_FILENAME> <OUT_MD_FILENAME>
    """


def is_empty(var) -> bool:
    """

    :param var:
    :return:
    """
    return len(var) == 0


def main():
    if not len(sys.argv) == 3:
        print(usage.__doc__.format(script=sys.argv[0]))
        sys.exit(0)

    csv_rows = []
    input_file = str(sys.argv[1])
    output_file = str(sys.argv[2])

    # pre-process input file
    os.system('bash sort.sh {input} --begin-line 2'.format(input=input_file))

    # read csv data
    with open(input_file, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            csv_rows.append(row)

    # # search phonetic symbols
    # for row in csv_rows:
    #     if not all(v for v in row):
    #         result = youdao.search_en_word(row[0])
    #         row[:] = [result['key'], result['uk'], result['us'], result['url'],
    #                   result['trans'][0][:12] + '...' if len(result['trans']) else '']

    # overwrite csv file
    with open(input_file, 'w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(csv_rows)

    # csv rows to markdown rows
    md_rows = [['', csv_rows[0][0], csv_rows[0][1], csv_rows[0][2], csv_rows[0][4]]]
    cnt = 0
    for row in csv_rows[1:]:
        cnt += 1
        md_rows.append(
            ['{} '.format(cnt),
             '[{}]({})'.format(row[0], row[3]),
             '`{}`'.format(row[1]) if len(row[1]) else '',
             '`{}`'.format(row[2]) if len(row[2]) else '',
             '`{}`'.format(row[4]) if len(row[4]) else '']
        )

    # write markdown file
    youdao.write_md_table(md_rows, output_file)


if __name__ == "__main__":
    main()
