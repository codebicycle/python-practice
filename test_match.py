"""
match.py is a grep-like utility.

Usage: match.py [OPTION]... PATTERN [FILE]...

See the docstring of each test_* function for specific requirements.

"""

from subprocess import Popen, PIPE
import os.path
import sys

HERE = os.path.dirname(__file__)


def call(*args, **kwargs):
    """Call match.py with the arguments in args. If the input keyword argument
    is given, send it to stdin. Return a (stdoutdata, stderrdata, returncode)
    tuple.

    """
    input = kwargs.get('input')
    encoding = kwargs.get('encoding', 'utf-8')
    command = (sys.executable, os.path.join(HERE, 'match.py')) + args
    p = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    if encoding and input is not None:
        input = input.encode(encoding)
    out, err = p.communicate(input)
    if encoding:
        out = out.decode(encoding)
        err = err.decode(encoding)
    return out, err, p.returncode


def test_basic(tmpdir):
    """Search the named input FILEs (or standard input if no files are named)
    for lines matching the given PATTERN (substring match). By default, print
    the matching lines.

    """
    tmpdir.chdir()
    tmpdir.join('one').write(b'one\n', 'wb')
    tmpdir.join('two').write(b'two\n', 'wb')
    assert call('o', input='zero\n') == ('zero\n', '', 0)
    assert call('o', 'one', input='zero\n') == ('one\n', '', 0)
    assert call('o', 'one', 'two') == ('one\ntwo\n', '', 0)


def test_status(tmpdir):
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


def test_newlines(tmpdir):
    """Lines are terminated by a line feed character ('\n'). If the last line
    to be output does not end in a newline, append one. If there are no lines
    (i.e. zero bytes), don't output anything.

    """
    assert call('t', input='one\ntwo\r\nthree\n') == ('two\r\nthree\n', '', 0)
    assert call('', input='one') == ('one\n', '', 0)
    assert call('', input='\n') == ('\n', '', 0)
    assert call('') == ('', '', 1)

