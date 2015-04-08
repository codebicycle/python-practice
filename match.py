#!/usr/bin/env python3

import sys

def opts_and_args(argv, supported_options):
    args = argv[1:]
    active_options = [opt for opt in supported_options if opt in args]

    for opt in active_options:
        while opt in args:
            args.remove(opt)

    return(active_options, args)


def is_matched(pattern, file, output_cb):
    matched = False
    for line in file:
        if pattern in line:
            matched = True
            output_cb(pattern, line)

    return matched


def default_output(pattern, line):
    print(line.decode().rstrip('\n'))


def only_matching_output(pattern, line):
    if not pattern:
        return
    for i in range(line.count(pattern)):
        print(pattern.decode())


if __name__ == "__main__":

    SUPPORTED_OPTIONS = ['-o', '--only-matching']
    options, args = opts_and_args(sys.argv, SUPPORTED_OPTIONS)

    try:
        pattern = args[0].encode('utf-8')
    except IndexError:
        exit(2)

    filenames = args[1:]

    if '-o' in options or '--only-matching' in options:
      cb = only_matching_output
    else:
      cb = default_output

    if len(filenames) < 1:
        matched = is_matched(pattern, sys.stdin.buffer, cb)
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
                    matched = is_matched(pattern, f, cb)
        if not matched:
            exit(1)
