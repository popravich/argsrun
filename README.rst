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
                'myproj = argsrun:main',  # argsrun will handle main command
            ],
            'myproj': [                   # ...and lookup for this subcommands
                'main = myproj:main',
                'run = myproj.module:run',
            ],
          })

In case you have several packages/projects and you want them to share same
entry point, you can easily do it like follows:

.. code:: python

    # my-frontend-app/setup.py

    setup(name="MySite Frontend",
          entry_points={
            'console_scripts': [
                'mysite = argsrun:main',
            ],
            'mysite': [
                'serve-frontend = frontend:serve',
            ]
          })

    # my-backend-app/setup.py

    setup(name="MySite Admin backend",
          entry_points={
            'console_scripts': [
                'mysite = argsrun:main',
            ],
            'mysite': [
                'serve-admin = backend:serve',
            ]
          })

     # In my-frontend-app/frontend/__init__.py

     import argsrun

     def handler(options):
         # Run frontend app
         pass

     def parser_setup(ap):
         ap.add_argument('--port', help="Port to bind to")

     main = argsrun.Entry(handler, parser_setup)
