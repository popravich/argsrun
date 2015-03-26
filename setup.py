import os
import re

from setuptools import find_packages, setup


def read_version():
    regexp = re.compile(r"^__version__\W*=\W*'([\d.abrc]+)'")
    init_py = os.path.join(os.path.dirname(__file__), 'argsrun', '__init__.py')
    with open(init_py) as f:
        for line in f:
            match = regexp.match(line)
            if match is not None:
                return match.group(1)
        else:
            raise RuntimeError('Cannot find version in argsrun/__init__.py')


install_requires = []

setup(name="Argsrun",
      version=read_version(),
      description="Simple library for creating commands & subcommands",
      platforms=["POSIX"],   # XXX
      packages=find_packages(),
      include_package_data=True,
      install_requires=install_requires,
      entry_points={
        'console_scripts': [
            'argsrun = argsrun:main',
            ],
        'argsrun': [
            'discover = argsrun.discover:discover',
            'echo = argsrun:echo',
            ],
        },
      )
