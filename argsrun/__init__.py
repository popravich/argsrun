import os
import sys
import argparse
import pkg_resources


__version__ = '0.0.2'


class Entry:
    """Creates argsrun entry.

    Entry holds command handler and optionally:
    * argparser_setup callable -- to configure sub-parser
    * short_help and description messages for parent parser.

    if no short_help or description are passed they will be extracted
    from handler's docstring (if any, ofcourse).

    The argsrun.Entry instances are callable objects so the following
    use-case is possible:

    >>> def handler(opts):
    ...     print(opts)
    >>> def setup(ap):
    ...     pass
    >>> main = argsrun.Entry(handler, setup)
    >>> if __name__ == '__main__':
    ...     main()
    """

    __slots__ = ('handler', 'argparser_setup',
                 'short_help', 'description')

    def __init__(self, handler, argparser_setup=None, *,
                 short_help=None, description=None):
        assert callable(handler), handler
        assert argparser_setup is None or callable(argparser_setup), \
            argparser_setup
        assert short_help is None or isinstance(short_help, str), short_help
        assert description is None or isinstance(description, str), \
            description
        self.handler = handler
        self.argparser_setup = argparser_setup
        docstr = getattr(handler, '__doc__', None)
        if docstr:
            # TODO: filter docstring (drop whitespaces)
            short = [l.strip() for l in docstr.splitlines() if l.strip()]
            short = short and short[0] or None
        else:
            short = None
        self.short_help = short_help or short
        self.description = description or docstr

    def __call__(self, argv=None):
        return runme(self, argv)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    script, *args = argv
    script = os.path.basename(script)

    # XXX: this is not very convenient way
    ep = list(pkg_resources.iter_entry_points('console_scripts', name=script))
    assert len(ep) > 0, "Unexpected run"

    # First lets collect all commands and check if any specified in argv
    ap = argparse.ArgumentParser(add_help=False)
    sub = ap.add_subparsers(title="Available commands", dest='command')

    entries = list(pkg_resources.iter_entry_points(script))
    for entry in entries:
        p = sub.add_parser(entry.name, add_help=False)
        p.set_defaults(entry_point=entry)
    opts, _ = ap.parse_known_args(args)

    def _prepare_command(entry_point, sub_parser, sub_setup=False):
        entry = entry_point.load()
        assert isinstance(entry, Entry)
        sub = sub_parser.add_parser(entry_point.name,
                                    description=entry.description,
                                    help=entry.short_help)
        if sub_setup and entry.argparser_setup:
            entry.argparser_setup(sub)
        return entry

    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(title="Available commands")

    if opts.command is None:
        for entry in entries:
            _prepare_command(entry, sub)
        ap.print_help()
        return -1

    try:
        entry = _prepare_command(opts.entry_point, sub, sub_setup=True)
        options = ap.parse_args(args)
        return entry.handler(options)
    except InvalidArguments as exc:
        print(exc)
        ap.print_help()
        return -1


def runme(handler, argv=None):
    """Runs standalone argsrun Entry."""
    assert isinstance(handler, Entry), handler
    if argv is None:
        argv = sys.argv
    script, *args = argv
    ap = argparse.ArgumentParser(description=handler.description)
    if handler.argparser_setup:
        handler.argparser_setup(ap)
    try:
        options = ap.parse_args(args)
        return handler.handler(options)
    except InvalidArguments as exc:
        print(exc)
        ap.print_help()
        return -1


# TODO: replace with argparse.ArgumentError
class InvalidArguments(Exception):
    """Exception to be raised in case of any option is invalid.

    First argument should be a text message.
    Help will be printed with that message.
    """
