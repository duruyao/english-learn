#!/usr/bin/env bash

## date:   2022-07-07
## author: duruyao@gmail.com
## desc:   command line game for typing practice

function info_ln() {
  printf "\033[1;32;32m%s\n\033[m" "${1}"
}

function trace_ln() {
  printf "\033[1;32;34m%s\n\033[m" "${1}"
}

function warning_ln() {
  printf "\033[1;32;33m%s\n\033[m" "${1}"
}

function error_ln() {
  printf "\033[1;32;31m%s\n\033[m" "${1}"
}

function sec2hms() {
  printf "%d:%02d:%02d" "$((10#$1 / 3600))" "$((10#$1 / 60 % 60))" "$((10#$1 % 60))"
}

function show_usage() {
  cat <<EOF
Usage: bash ${exec} [OPTIONS]

Command line game for typing practice

Options:
  -b, --batch=<N>                   Set batch size (default: 100)
  -d, --diff=<easy|normal|hard>     Select game difficulty (default: easy)
  -l, --length=<N>                  Set length of random string (default: 1)
  -h, --help                        Display this help message

Examples:
  bash ${exec}
  bash ${exec} -l 1 -b 100 -d easy
  bash ${exec} --length=1 --batch=100 --diff=easy

EOF
}

exec="$(realpath "$0")"
diff="easy"
length=1
batch=100

thesaurus=(
  "a-z,./;"
  "A-Za-z0-9,./;"
  "A-Za-z0-9,./;!\"#$%&\'()*+-:<=>?@[\\\\]^_\`{|}~"
)
chars="${thesaurus[0]}"

while (($#)); do
  case "$1" in
  -b | --batch)
    if [ -z "$2" ] || ! [[ $2 =~ ^[0-9]+$ ]]; then
      error_ln "Error: '$1' requires an integer argument" >&2
      show_usage >&2
      exit 1
    fi
    batch=$2
    shift 2
    ;;

  --batch=?*)
    if ! [[ ${1#*=} =~ ^[0-9]+$ ]]; then
      error_ln "Error: '$1' requires an integer argument" >&2
      show_usage >&2
      exit 1
    fi
    batch=${1#*=}
    shift 1
    ;;

  -d | --diff)
    if [ -z "$2" ] || ! [[ $2 =~ ^(EASY|NORMAL|HARD|easy|normal|hard)$ ]]; then
      error_ln "Error: '$1' requires a known argument (easy|normal|hard)" >&2
      show_usage >&2
      exit 1
    fi
    diff="$2"
    shift 2
    ;;

  --diff=?*)
    if ! [[ "${1#*=}" =~ ^(EASY|NORMAL|HARD|easy|normal|hard)$ ]]; then
      error_ln "Error: Unknown argument: '$2'" >&2
      show_usage >&2
      exit 1
    fi
    diff="${1#*=}"
    shift 1
    ;;

  -l | --length)
    if [ -z "$2" ] || ! [[ $2 =~ ^[0-9]+$ ]]; then
      error_ln "Error: '$1' requires an integer argument" >&2
      show_usage >&2
      exit 1
    fi
    length=$2
    shift 2
    ;;

  -l=?* | --length=?*)
    if ! [[ ${1#*=} =~ ^[0-9]+$ ]]; then
      error_ln "Error: '$1' requires an integer argument" >&2
      show_usage >&2
      exit 1
    fi
    length=${1#*=}
    shift 1
    ;;

  -h | --help)
    show_usage
    exit 0
    ;;

  --* | -* | *)
    error_ln "Error: Unknown flag: '$1'" >&2
    show_usage >&2
    exit 1
    ;;
  esac
done

if [ "${diff}" == "normal" ]; then
  chars="${thesaurus[1]}"
elif [ "${diff}" == "hard" ]; then
  chars="${thesaurus[2]}"
fi

level="${diff}-${length}-${batch}"
history="${HOME}/.qwer/${level}.md"
mkdir -p "$(dirname "${history}")"

if ! [ -f "${history}" ]; then
  {
    printf "%s\n" "| SCORE  | LEVEL          | DATE                | GAMER            |"
    printf "%s\n" "|--------|----------------|---------------------|------------------|"
  } >>"${history}"
fi

gain=0
loss=0
gamer="someone"

for i in 3 2 1 Go; do
  printf "%-2s!\n" "${i}"
  sleep 1
done
echo

for ((cnt = 1; cnt <= "${batch}"; cnt++)); do
  word="$(LC_ALL=C tr -dc "${chars}" </dev/urandom | head -c "${length}")"
  printf "[%3s]\n" "${cnt}"
  input=""
  begin="$(TZ=UTC-8 date "+%Y-%m-%d %H:%M:%S")"
  while [ "${input}" != "${word}" ]; do
    printf "      Q: "
    trace_ln "${word}"
    printf "      A: "
    read -r input
  done
  end="$(TZ=UTC-8 date "+%Y-%m-%d %H:%M:%S")"
  duration="$(("$(date +%s -d "${end}")" - "$(date +%s -d "${begin}")"))"
  printf "      T: "
  if [ ${duration} -gt "${length}" ]; then
    warning_ln "$(sec2hms "${duration}")"
    loss=$((loss + 1))
  else
    info_ln "$(sec2hms "${duration}")"
    gain=$((gain + 1))
  fi
done

score="$(echo "(${gain}*100)/(${gain}+${loss})" | bc -l)"

printf "\n"
printf "SCORE: %.2f\n" "${score}"
printf "YOUR NAME: "
read -r name
if [ -n "${name}" ]; then
  gamer="$(echo "${name}" | head -c 16)"
fi

date="$(TZ=UTC-8 date "+%Y-%m-%d %H:%M:%S")"
temp="/tmp/$(date | md5sum | head -c 32).tmp"
cp "${history}" "${temp}"
printf "| %06.2f | %-14s | %-19s | %-16s | <-\n" "${score}" "${level}" "${date}" "${gamer}" >>"${temp}"

echo "HISTORY:"
awk "NR <=2" "${temp}" | sed "s/^/         /g"
awk "NR >=3" "${temp}" | sed "s/^/         /g" | sort -r
rm -f "${temp}"
printf "| %06.2f | %-14s | %-19s | %-16s |\n" "${score}" "${level}" "${date}" "${gamer}" >>"${history}"
echo ""
