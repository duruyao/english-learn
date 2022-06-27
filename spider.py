import os
import sys
import csv


def empty(var) -> bool:
    return len(var) == 0


def search_pronunciations(word: str) -> tuple[str, str]:
    en_pronunciation, us_pronunciation = word, word
    # TODO: finish it
    #
    return en_pronunciation, us_pronunciation


def column_widths(rows: list[list[str]]) -> list[int]:
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


def csv_to_md_table(rows: list[list[str]]) -> list[str]:
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
            line += (' {:<' + str(widths[idx]) + '} |').format(item)
            idx += 1
        table.append(line)

    # generate
    table[0], table[1] = table[1], table[0]
    return table


def main():
    data = []
    input_file = str(sys.argv[1])
    output_file = str(sys.argv[2])

    # pre-process input file
    os.system('bash sort.sh ' + input_file + ' --begin-line 1')

    # read csv data
    with open(input_file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            data.append(row)
    print(data)

    # search pronunciations
    for row in data:
        if len(row) < 3 or empty(row[1]) or empty(row[2]):
            row[1:] = [*search_pronunciations(row[0])]

    # overwrite csv file
    with open(input_file + '.tmp', 'w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(data)

    # csv to md table
    table = csv_to_md_table(data)
    for row in table:
        print(row)

    # write md file
    # TODO: finish it
    #


if __name__ == "__main__":
    main()
