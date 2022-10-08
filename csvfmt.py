#!/usr/bin/env python3.9

import sys
import csv
import youdao


def usage():
    """Usage:
    python3 {script} <IN_CSV_FILENAME> <OUT_TXT_FILENAME>
    """


def main():
    if not len(sys.argv) == 3:
        print(usage.__doc__.format(script=sys.argv[0]))
        sys.exit(0)

    sep = '  '
    input_file = str(sys.argv[1])
    output_file = str(sys.argv[2])

    rows = []
    with open(input_file, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        for line in reader:
            rows.append(line)

    lines = []
    widths = youdao.column_widths(rows)
    for row in rows:
        line = []
        for i in range(len(row)):
            line.append(('{:<' + str(widths[i]) + '}').format(row[i]))
        lines.append(line)

    with open(output_file, 'w') as file:
        for line in lines:
            file.write('%s\n' % sep.join(line))


if __name__ == "__main__":
    main()
