#!/usr/bin/env python3

import sys

if __name__ == "__main__":

    try:
        patern = sys.argv[1].encode('utf-8')
    except IndexError:
        exit(2)

    filenames = sys.argv[2:]

    if len(filenames) < 1:
        match = False
        for line in sys.stdin.buffer:
            if patern in line:
                match = True
                print(line.decode().rstrip('\n'))
        if not match:
            exit(1)
    else:
        match = False
        for filename in filenames:
            try:
                f = open(filename, mode="rb")
            except OSError:
                exit(2)
            else:
                with  f:
                    for line in f:
                        if patern in line:
                            match = True
                            print(line.decode().rstrip('\n'))
        if not match:
            exit(1)
