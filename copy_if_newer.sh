#!/bin/bash
if [ ! -e "$1" ]; then
    echo "Error: Source File $1 does not exist" >&2
    exit 1
elif [ ! -e "$2" ]; then
    cp "$1" "$2"
    echo "Copied $1 to $2"
    exit 0
elif [ "$1" -nt "$2" ]; then
        cp "$1" "$2"
        echo "$1 is newer than $2. Copied $1 to $2"
        exit 0
else
    echo " $1 is not newer than $2"
    exit 0
fi