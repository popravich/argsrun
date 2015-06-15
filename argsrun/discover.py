import pkg_resources
import argsrun


@argsrun.Entry
def discover(options):
    """Discovers installed commands."""
    for entry in pkg_resources.iter_entry_points('console_scripts'):
        if entry.module_name == __package__:
            print(entry.name)
        # TODO: add options and display more info about commands.
        # print(entry.name, entry.module_name, entry.attrs)
        # print(__package__)
        # break

if __name__ == '__main__':
    argsrun.runme(discover)
