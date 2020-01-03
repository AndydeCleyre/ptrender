#!/bin/sh -e
trap "cd $PWD" EXIT
cd "$(dirname "$0")"

ptrender -h > ptrender_help.txt
vwrite -h | sed -E 's:(root_path=)[^]]+(\]):\1<CWD>\2:g' > vwrite_help.txt

python3 -c "
from json import loads, dumps

try: data = loads(open('vars_readme.json').read())
except FileNotFoundError: data = {}

for doc in ('ptrender_help', 'vwrite_help'):
    with open(f'{doc}.txt') as helpfile:
        data.update({f'{doc}': helpfile.read()})

with open('vars_readme.json', 'w') as varsfile:
    varsfile.write(dumps(data))
"

rm {ptrender,vwrite}_help.txt
