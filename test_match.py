"""
match.py is a grep-like utility.

Usage: match.py [OPTION]... PATTERN [FILE]...

See the docstring of each test_* function for specific requirements.

"""


def test_basic(call, tmpdir):
    """Search the named input FILEs (or standard input if no files are named)
    for lines matching the given PATTERN (substring match). By default, print
    the matching lines.

    """
    tmpdir.chdir()
    tmpdir.join('one').write(b'one\n', 'wb')
    tmpdir.join('two').write(b'two\n', 'wb')
    assert call('o', input='zero\n') == ('zero\n', '', 0)
    assert call('o', 'one', input='zero\n') == ('one\n', '', 0)
    # prefix output lines with the file name when working with multiple files
    assert call('o', 'one', 'two') == ('one:one\ntwo:two\n', '', 0)
    assert call('e', input='ONE') == ('', '', 1)
    assert call('E', input='one') == ('', '', 1)


def test_status(call, tmpdir):
    """Exit with status 0 if any matches are found and with 1 if not.
    Exit with status 2 in case of error.

    """
    tmpdir.chdir()
    assert call('o', input='one\n') == ('one\n', '', 0)
    assert call('x', input='one\n') == ('', '', 1)

    # three doesn't exist
    out, err, status = call('x', 'three')
    assert out == ''
    assert status == 2

    # no pattern is given
    out, err, status = call()
    assert out == ''
    assert status == 2


def test_newlines(call, tmpdir):
    """Lines are terminated by a line feed character ('\\n'). If the last line
    to be output does not end in a newline, append one. If there are no lines
    (i.e. zero bytes), don't output anything.

    """
    assert call('t', input='one\ntwo\r\nthree\n') == ('two\r\nthree\n', '', 0)
    assert call('', input='one') == ('one\n', '', 0)
    assert call('', input='\n') == ('\n', '', 0)
    assert call('') == ('', '', 1)


def test_no_encoding(call, tmpdir):
    """match.py is not encoding-aware; it operates on binary data (bytes in,
    bytes out).

    """
    ae_bytes = 'aeæ\n'.encode('latin-1')
    tmpdir.chdir()
    tmpdir.join('one').write(ae_bytes, 'wb')
    assert call('a', input=ae_bytes, encoding=None) == (ae_bytes, b'', 0)
    assert call('a', 'one', encoding=None) == (ae_bytes, b'', 0)


def test_only_matching(call):
    """`-o`, `--only-matching`: print only the matched (non-empty) parts of
    a matching line, with each such part on a separate output line.

    """
    assert call('-o', '', input='zero') == ('', '', 0)
    assert call('-o', 'e', input='one') == ('e\n', '', 0)
    assert call('-o', 'e', input='two') == ('', '', 1)
    assert call('-o', 'e', input='three') == ('e\ne\n', '', 0)


def test_invert_match(call):
    """`-v`, `--invert-match`: invert the sense of matching, to select
    non-matching lines.

    """
    assert call('-v', '', input='zero') == ('', '', 1)
    assert call('-v', 'e', input='one') == ('', '', 1)
    assert call('-v', 'e', input='two') == ('two\n', '', 0)
    assert call('-v', 'e', input='one\ntwo\n') == ('two\n', '', 0)


def test_ignore_case(call):
    """`-i`, `--ignore-case`: ignore case distinctions in both the PATTERN
    and the input files.

    """
    assert call('-i', '', input='zero') == ('zero\n', '', 0)
    assert call('-i', 'e', input='one') == ('one\n', '', 0)
    assert call('-i', 'e', input='ONE') == ('ONE\n', '', 0)
    assert call('-i', 'E', input='one') == ('one\n', '', 0)
    assert call('-i', 'E', input='ONE') == ('ONE\n', '', 0)
    assert call('-i', 'e', input='two') == ('', '', 1)


def test_regexp(call, tmpdir):
    """`-e PATTERN`, `--regexp=PATTERN`: use PATTERN as the pattern. This
    can be used to specify multiple search patterns, or to protect a pattern
    beginning with a hyphen (-).

    """
    assert call('-e', '-o', input='-one') == ('-one\n', '', 0)
    assert call('-o', '-e', 'e', '-e', 'o', input='one') == ('o\ne\n', '', 0)

    # when -e is used, all arguments are FILE(s) (there's no PATTERN)
    tmpdir.chdir()
    tmpdir.join('e').write('three')
    assert call('e', '-e', 'e', input='one') == ('three\n', '', 0)


def test_no_filename(call, tmpdir):
    """`-h`, `--no-filename`: suppress the prefixing of file names on output.
    This is the default when there is only one file (or only standard input)
    to search.

    """
    tmpdir.chdir()
    tmpdir.join('one').write(b'one\n', 'wb')
    tmpdir.join('two').write(b'two\n', 'wb')
    assert call('-h', 'o', 'one', 'two') == ('one\ntwo\n', '', 0)

