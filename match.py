#!/usr/bin/env python3

import sys

if __name__ == "__main__":

    try:
        patern = sys.argv[1]
    except:
        exit(2)

    filenames = sys.argv[2:]

    if len(filenames) < 1:
        line = input()
        if patern in line:
            print(line)
        else:
            exit(1)
    else:
        match = False
        for filename in filenames:
            try:
                f = open(filename)
            except OSError:
                exit(2)
            else:
                with  f:
                    for line in f:
                        if patern in line:
                            match = True
                            print(line, end='')
        if not match:
            exit(1)
