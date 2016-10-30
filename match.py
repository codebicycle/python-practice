#!/usr/bin/env python3

import sys
import re
import click


def iter_files(paths):
    for path in paths:
        try:
            yield open(path, 'rb')
        except (IOError, OSError) as e:
            print("error: {}".format(e), file=sys.stderr)


def common_options(f):
    @click.command()
    @click.option(
        '-e', '--regexp', multiple=True, metavar='PATTERN',
        help=('use PATTERN for matching')
    )
    @click.option(
        '-h', '--no-filename', is_flag=True,
        help=('suppress the file name prefix on output')
    )
    @click.option(
        '-i', '--ignore-case', is_flag=True,
        help=('ignore case distinctions')
    )
    @click.option(
        '-o', '--only-matching', is_flag=True,
        help=('show only the part of a line matching PATTERN')
    )
    @click.option(
        '-v', '--invert-match', is_flag=True,
        help=('select non-matching lines')
    )
    def wrapper(**kwargs):
        '''Search for PATTERN in each FILE or standard input.'''
        f(**kwargs)

    return wrapper


@click.argument('file', nargs=-1, type=click.Path(exists=True))
@click.argument('pattern', required=False)
@common_options
def match(pattern, file, **kwargs):
    '''Search for PATTERN in each FILE or standard input.'''
    # print('match: pattern:', pattern)
    # print('match: file:', file)
    # print('match: kwargs:', kwargs)

    if kwargs['regexp']:
        match_regexp()
    else:
        match_helper(pattern, file, **kwargs)


@click.argument('file', nargs=-1, type=click.Path(exists=True))
@common_options
def match_regexp(file, **kwargs):
    # print('match-regexp: file:', file)
    # print('match-regexp: kwargs:', kwargs)

    pattern = kwargs['regexp']
    match_helper(pattern, file, **kwargs)


def match_helper(pattern, file, **kwargs):
    # print('match_helper: pattern:', pattern)
    # print('match_helper: file:', file)
    # print('match_helper: kwargs:', kwargs)

    if pattern is None:
        sys.exit(2)

    opt_no_filename = kwargs.get('no_filename')
    opt_only_matching = kwargs.get('only_matching')
    opt_ignore_case = kwargs.get('ignore_case')
    opt_invert_match = kwargs.get('invert_match')

    def output():
        if opt_no_filename or len(file) <= 1:
            filename = b''
        else:
            filename = '{}:'.format(f.name).encode('utf8')

        if opt_only_matching:
            if pat:
                for m in re.findall(pat, line, flag):
                    out = filename + m + b'\n'
                    sys.stdout.buffer.write(out)
        else:
            out = filename + line.rstrip(b'\n') + b'\n'
            sys.stdout.buffer.write(out)


    if type(pattern) is tuple:
        patterns = [pat.encode('utf8') for pat in pattern[::-1]] 
    else:
        patterns = [pattern.encode('utf8')]

    if file:
        files = iter_files(file)
    else:
        files = (sys.stdin.buffer,)

    flag = re.IGNORECASE if opt_ignore_case else 0

    matched = False
    for f in files:
        for line in f:
            for pat in patterns:
                found = re.search(pat, line, flag)
                if opt_invert_match:
                    if not found:
                        output()
                        matched = True
                elif found:
                    output()
                    matched = True
        f.close()
    if not matched:
        sys.exit(1)


def main(*args):
    match()


if __name__ == "__main__":

    main()
