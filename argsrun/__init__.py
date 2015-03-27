import os
import sys
import argparse
import pkg_resources


__version__ = '0.0.1'


def main():
    script, *args = sys.argv
    script = os.path.basename(script)

    # XXX: this is not very convenient way
    ep = list(pkg_resources.iter_entry_points('console_scripts', name=script))
    assert len(ep) > 0, "Unexpected run"

    ap = argparse.ArgumentParser(add_help=False)
    sub = ap.add_subparsers(title="Available commands", dest='command')

    entries = list(pkg_resources.iter_entry_points(script))
    for entry in entries:
        p = sub.add_parser(entry.name, add_help=False)
        p.set_defaults(entry_point=entry)
    opts, tail = ap.parse_known_args(args)

    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(title="Available commands")

    if opts.command is None:
        for entry in entries:
            _build_sub_parser(entry, sub)
        ap.print_help()
        return -1

    prepare_func, p = _build_sub_parser(opts.entry_point, sub)
    handler = prepare_func(p)
    assert callable(handler), (
        "{!s} entry must return callable object".format(entry))
    options = ap.parse_args(args)
    try:
        return handler(options)
    except InvalidArguments as exc:
        print(exc)
        ap.print_help()
        return -1


def _build_sub_parser(entry, sub_parser):
    prepare_func = entry.load()
    docstr = getattr(prepare_func, '__doc__', None)
    if docstr:
        short_help = [l.strip() for l in docstr.splitlines() if l.strip()][0]
    else:
        short_help = None
    sub = sub_parser.add_parser(entry.name, description=docstr,
                                help=short_help)
    return prepare_func, sub


class InvalidArguments(Exception):
    """Exception to be raised in case of any option is invalid.

    First argument should be a text message.
    Help will be printed with that message.
    """


def echo(ap):
    """Sample command.

    Prints "Hello, World!" or any message you pass as extra arguments.
    """
    ap.add_argument('message', nargs='*', default="Hello, World!".split(),
                    help="Message to print")

    def handler(options):
        print(' '.join(options.message))

    return handler
