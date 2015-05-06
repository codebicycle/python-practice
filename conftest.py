from subprocess import Popen, PIPE
import os.path
import sys

HERE = os.path.dirname(__file__)
MATCH_PY = (sys.executable, os.path.join(HERE, 'match.py'))


def pytest_addoption(parser):
    parser.addoption("--grep", action="store_true",
        help="run tests against grep")


def pytest_generate_tests(metafunc):
    if 'call' in metafunc.fixturenames:
        call = None
        if metafunc.config.option.grep:
            call = grep
        if not call:
            call = match_py
        metafunc.parametrize("call", [call], ids=[call.__name__])


def match_py(*args, input=None, encoding='utf-8'):
    return call_subprocess(MATCH_PY, args, input, encoding)

def grep(*args, input=None, encoding='utf-8'):
    return call_subprocess('grep', args, input, encoding)


def call_subprocess(command, args, input=None, encoding='utf-8'):
    """Call command with the arguments in args. If the input keyword argument
    is given, send it to stdin. Return a (stdoutdata, stderrdata, returncode)
    tuple.

    """
    if isinstance(command, str):
        command = (command, )
    command = command
    p = Popen(command + args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    if encoding and input is not None:
        input = input.encode(encoding)
    out, err = p.communicate(input)
    if encoding:
        out = out.decode(encoding)
        err = err.decode(encoding)
    return out, err, p.returncode

