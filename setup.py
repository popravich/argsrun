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


def read(*parts):
    with open(os.path.join(*parts), 'rt') as f:
        return f.read().strip()


install_requires = []

classifiers = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: POSIX',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries',
    'Topic :: Utilities',
]

setup(name="argsrun",
      version=read_version(),
      description="Simple tool for creating commands & sub-commands",
      long_description="\n\n".join((read('README.rst'),)),
      classifiers=classifiers,
      platforms=["POSIX"],   # XXX
      author="Alexey Popravka",
      author_email="alexey.popravka@horsedevel.com",
      packages=find_packages(),
      include_package_data=True,
      install_requires=install_requires,
      url="https://github.com/popravich/argsrun",
      license="MIT",
      entry_points={
        'console_scripts': [
            'argsrun = argsrun:main',
            ],
        'argsrun': [
            'discover = argsrun.discover:discover',
            ],
        },
      )
