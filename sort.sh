#!/usr/bin/env bash

## date:   2022-06-27
## author: duruyao@gmail.com
## desc:   sort lines in a file

set -euo pipefail

function error_ln() {
  printf "\033[1;32;31m%s\n\033[m" "$1"
}

function warning_ln() {
  printf "\033[1;33m%s\n\033[m" "$1"
}

function info_ln() {
  printf "\033[0;32;32m%s\n\033[m" "$1"
}

function show_usage() {
  cat <<EOF
Usage: bash sort.sh [OPTIONS] INPUT_FILENAME

Sort from line X to line Y in a file

Options:
      --begin-line NUM          Beginning line number (default: 0)
      --end-line NUM            Ending line number (default: UINT32_MAX)
  -h, --help                    Display this help message
      --output PATH             Output filename (default: INPUT_FILENAME)

EOF
}

input_filename=
output_filename=
output_filename_tmp="${PWD}/$(date | md5sum | head -c 32).tmp"
begin_line=0
end_line=4294967295

while (($#)); do
  case "$1" in
  --begin-line)
    if [ -z "$2" ]; then
      error_ln "Error: '$1' requires a non empty argument" >&2
      show_usage >&2
      exit 1
    fi
    begin_line="$2"
    shift 2
    ;;

  --end-line)
    if [ -z "$2" ]; then
      error_ln "Error: '$1' requires a non empty argument" >&2
      show_usage >&2
      exit 1
    fi
    end_line="$2"
    shift 2
    ;;

  -h | --help)
    show_usage
    exit 0
    ;;

  --output)
    if [ -z "$2" ]; then
      error_ln "Error: '$1' requires a non empty argument" >&2
      show_usage >&2
      exit 1
    fi
    if ! [ -f "$2" ]; then
      error_ln "Error: No such file: '$2'" >&2
      show_usage >&2
      exit 1
    fi
    output_filename="$2"
    shift 2
    ;;

  --* | -*)
    error_ln "Error: Unknown flag: '$1'" >&2
    show_usage >&2
    exit 1
    ;;

  *)
    if ! [ -f "$1" ]; then
      error_ln "Error: No such file: '$1'" >&2
      show_usage >&2
      exit 1
    fi
    input_filename="$1"
    shift 1
    ;;
  esac
done

if [ -z "${input_filename}" ]; then
  error_ln "Error: Missing INPUT_FILENAME" >&2
  show_usage >&2
  exit 1
fi

if [ -z "${output_filename}" ]; then
  output_filename="${input_filename}"
fi

awk "NR < ${begin_line}" "${input_filename}" >"${output_filename_tmp}"
awk "NR >= ${begin_line} && NR <= ${end_line}" "${input_filename}" | LC_COLLATE=C sort --ignore-case | uniq >>"${output_filename_tmp}"
awk "NR > ${end_line}" "${input_filename}" >>"${output_filename_tmp}"
mv "${output_filename_tmp}" "${output_filename}"
