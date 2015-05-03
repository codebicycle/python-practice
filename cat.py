"""
Usage: cat.py [FILE]...
Concatenate FILE(s), or standard input, to standard output.

"""
import sys


def iter_files(paths):
    for path in paths:
        try:
            yield open(path, 'rb')
        except (IOError, OSError) as e:
            print("error: {}".format(e), file=sys.stderr)


def main(argv=None):
    if not argv:
        argv = list(sys.argv)

    if len(argv) < 2:
        files = [sys.stdin.buffer]
    else:
        files = iter_files(argv[1:])

    for file in files:
        for line in file:
            sys.stdout.buffer.write(line)
        file.close()


if __name__ == "__main__":

    main()

