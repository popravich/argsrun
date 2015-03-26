import pkg_resources


def discover(ap):
    """Discovers installed commands."""
    return handler


def handler(options):
    for entry in pkg_resources.iter_entry_points('console_scripts'):
        if entry.module_name == __package__:
            print(entry.name)
        # print(entry.name, entry.module_name, entry.attrs)
        # print(__package__)
        # break
    pass
