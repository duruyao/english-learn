#!/usr/bin/env bash

set -xeuo pipefail

app_home="${PWD}"
chmod +x ./*.py
pip3 install -r requirements.txt
pushd /usr/local/bin >/dev/null
sudo rm -f trans youdao
sudo ln -s "${app_home}"/trans.py trans
sudo ln -s "${app_home}"/youdao.py youdao
popd >/dev/null
