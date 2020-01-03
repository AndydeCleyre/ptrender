#!/bin/sh
trap "cd $PWD" EXIT
cd "$(dirname "$0")"

./help.sh

ptrender -f ../README.rst.t vars_readme.json
