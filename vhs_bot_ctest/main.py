# main.py

import click

from vhs_bot_ctest.browse.registry import BrowserRegistry


@click.command()
@click.option(
    "--course",
    default=None,
    required=True,
    help="Course name.",
    type=click.Choice(BrowserRegistry.get_names(), case_sensitive=True),
)
@click.option(
    "--agent",
    default=None,
    help="User agent string.",
)
def main(course, agent):
    """Check the availability of free slots for courses and tests at VHS schools."""
    # TODO: introduce a watch mode
    # TODO: notify the user about the availability of a place
    # TODO: allow overriding browser config in playwright via ENV vars or CLI args
    browser = BrowserRegistry.get_browser(course)
    if browser.is_place_available(agent=agent):
        print("Place is available.")
    else:
        print("No place available.")
