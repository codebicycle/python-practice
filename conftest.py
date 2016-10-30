from subprocess import Popen, PIPE
import os.path
import sys
import os

import py.io
import py.path

HERE = os.path.dirname(__file__)


def match_script(*args, input=None, encoding='utf-8'):
    command = (sys.executable, '-m', 'match')
    env = dict(os.environ)
    env['PYTHONPATH'] = HERE + ':' + env.get('PYTHONPATH', '')
    return call_subprocess(command, args, input, encoding, env)

def match_main(*args, input=None, encoding='utf-8'):
    import match
    return call_function(match.main, args, input, encoding)

def grep(*args, input=None, encoding='utf-8'):
    return call_subprocess('grep', args, input, encoding)

def pytest_addoption(parser):
    parser.addoption('--match-script', action='store_true',
        help="run the match module as a script (default)")
    parser.addoption('--match-main', action='store_true',
        help="run match.main() in the same interpreter")
    parser.addoption("--grep", action="store_true",
        help="run the tests against grep")
    parser.addoption("--all", action="store_true",
        help="all of the above")

def pytest_generate_tests(metafunc):
    if 'call' in metafunc.fixturenames:
        if metafunc.config.option.all:
            funcs = [grep, match_main, match_script]
        else:
            funcs = []
            if metafunc.config.option.match_script:
                funcs.append(match_script)
            if metafunc.config.option.match_main:
                funcs.append(match_main)
            if metafunc.config.option.grep:
                funcs.append(grep)
        if not funcs:
            funcs.append(match_script)
        ids = [f.__name__ for f in funcs]
        metafunc.parametrize("call", funcs, ids=ids)


def call_subprocess(command, args, input=None, encoding='utf-8', env=None):
    """Call command with the arguments in args. If the input keyword argument
    is given, send it to stdin. Return a (stdoutdata, stderrdata, returncode)
    tuple.

    """
    if isinstance(command, str):
        command = (command, )
    command = command
    p = Popen(command + args, stdin=PIPE, stdout=PIPE, stderr=PIPE, env=env)
    if encoding and input is not None:
        input = input.encode(encoding)
    out, err = p.communicate(input)
    if encoding:
        out = out.decode(encoding)
        err = err.decode(encoding)
    return out, err, p.returncode


def call_function(func, args, input=None, encoding='utf-8'):
    """Call func with the single argument args and capture stdout/err writes
    while it runs. Ignore SystemExit. If the input keyword argument is given,
    send it to stdin. Return a (stdoutdata, stderrdata, returncode) tuple.

    """
    tmpdir = py.path.local.mkdtemp()
    in_path = tmpdir.join('in')
    out_path = tmpdir.join('out')
    err_path = tmpdir.join('err')

    if input:
        if encoding:
            in_path.write_binary(input.encode(encoding))
        else:
            in_path.write_binary(input)
    else:
        in_path.ensure()

    in_capture = py.io.FDCapture(0, in_path.open('rb'), patchsys=True)
    out_capture = py.io.FDCapture(1, out_path.open('wb+'), patchsys=True)
    err_capture = py.io.FDCapture(2, err_path.open('wb+'), patchsys=True)

    code = 0
    try:
        func(args)
    except SystemExit as e:
        code = e.code

    in_capture.done()
    out_capture.done()
    err_capture.done()

    out = out_path.read_binary()
    err = err_path.read_binary()
    if encoding:
        out = out.decode(encoding)
        err = err.decode(encoding)

    return out, err, code

