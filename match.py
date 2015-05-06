#!/usr/bin/env python3

import sys
import click


def iter_files(paths):
    for path in paths:
        try:
            yield open(path, 'rb')
        except (IOError, OSError) as e:
            print("error: {}".format(e), file=sys.stderr)


@click.command()
@click.option(
    '-o', '--only-matching', is_flag=True,
    help=('show only the part of a line matching PATTERN')
)
@click.option(
    '-h', '--no-filename', is_flag=True,
    help=('suppress the file name prefix on output')
)
@click.option(
    '-v', '--invert-match', is_flag=True,
    help=('select non-matching lines')
)
@click.argument('pattern')
@click.argument('file', nargs=-1, type=click.Path(exists=True))
def main(pattern, file, **kwargs):
    '''Search for PATTERN in each FILE or standard input.'''
    # print(kwargs)
    # print('pattern:', pattern)
    # print('file:', file)

    def output():
        if kwargs['no_filename'] or len(file) <= 1:
            filename = b''
        else:
            filename = '{}:'.format(f.name).encode('utf8')

        if kwargs['only_matching']:
            if not pattern:
                return
            out = b''
            for i in range(line.count(pattern)):
                out += filename + pattern + b'\n'
        else:
            out = filename + line.rstrip(b'\n') + b'\n'

        sys.stdout.buffer.write(out)


    pattern = pattern.encode('utf8')

    if file:
        files = iter_files(file)
    else:
        files = (sys.stdin.buffer,)

    matched = False
    for f in files:
        for line in f:
            if kwargs['invert_match']:
                if pattern not in line:
                    sys.stdout.buffer.write(line.rstrip(b'\n') + b'\n')
                    matched = True
            elif pattern in line:
                output()
                matched = True
        f.close()
    if not matched:
        sys.exit(1)


if __name__ == "__main__":

    main()
