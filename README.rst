Argsrun
=======


Simple tool for creating pluggable commands and sub-commands.

Usage example:

.. code:: python

    # in setup.py of your project specify argsrun entry point in console scripts
    # and provided commands as follows:

    setup(name="MyProj",
          # ...
          entry_points={
            'console_scripts': [
                'myproj = argsrun:main',
            ],
            'myproj': [
                'main = myproj:main',
                'run = myproj.module:run',
            ],
          })

In case you have several packages/projects and you want them to share same
entry point, you can easily do it like follows:

.. code:: python

    # my-site/frontend/setup.py

    setup(name="MySite Frontend",
          entry_points={
            'console_scripts': [
                'mysite = argsrun:main',
            ],
            'mysite': [
                'server-frontend = frontend:serve',
            ]
          })

    # my-site/backend/setup.py

    setup(name="MySite Admin backend",
          entry_points={
            'console_scripts': [
                'mysite = argsrun:main',
            ],
            'mysite': [
                'server-admin = backend:serve',
            ]
          })
