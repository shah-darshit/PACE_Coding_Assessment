#!/bin/bash
if [ $# -lt 2 ]; then
    echo "Error: At least 2 files are required" >&2
    exit 1
fi

newest_file=$1
for i in "$@"; do
    if [ "$i" -nt "$newest_file" ]; then
        newest_file=$file
    fi
done
echo "$newest_file"