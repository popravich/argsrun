import os
import sys
import argparse
import pkg_resources


def main():
    script, *args = sys.argv
    script = os.path.basename(script)

    ep = list(pkg_resources.iter_entry_points('console_scripts', name=script))
    assert len(ep) > 0, "Unexpected run"

    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(title="Commands")
    for ep in pkg_resources.iter_entry_points(script):
        sub.add_parser(ep.name)

        print(ep.name, '=>', ep, type(ep))
        cmd = ep.load()
        print(cmd)

    res = ap.parse_known_args()
    print(res)


def version(*args, **kw):
    print("in version")
    print(args)
    print(kw)
