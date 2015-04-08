#!/usr/bin/env python3

import sys

def is_matched(pattern, file):
    matched = False
    for line in file:
        if pattern in line:
            matched = True
            print(line.decode().rstrip('\n'))

    return matched


if __name__ == "__main__":

    try:
        pattern = sys.argv[1].encode('utf-8')
    except IndexError:
        exit(2)

    filenames = sys.argv[2:]

    if len(filenames) < 1:
        matched = is_matched(pattern, sys.stdin.buffer)
        if not matched:
            exit(1)
    else:
        for filename in filenames:
            try:
                f = open(filename, mode="rb")
            except OSError:
                exit(2)
            else:
                with  f:
                    matched = is_matched(pattern, f)
        if not matched:
            exit(1)
