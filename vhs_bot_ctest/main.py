# main.py
import time

import click
import structlog

from vhs_bot_ctest.browse.registry import BrowserRegistry

FIVE_MINUTES_SECONDS = 5 * 60


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
@click.option(
    "--watch",
    default=False,
    help="Watch mode.",
    is_flag=True,
)
@click.option(
    "--check-interval",
    default=FIVE_MINUTES_SECONDS,
    help=f"Check interval in seconds (default {FIVE_MINUTES_SECONDS} seconds).",
)
def main(course, agent, watch=False, check_interval=60):
    """Check the availability of free slots for courses and tests at VHS schools."""
    # TODO: introduce a watch mode
    # TODO: notify the user about the availability of a place, e.g. via telegram (configure using ENV vars)
    #    package telegram-notification seems easy to use
    # TODO: allow overriding browser config in playwright via ENV vars or CLI args
    logger = structlog.get_logger(course=course)
    if agent:
        logger = logger.bind(agent=agent)
    if watch:
        while True:
            browser = BrowserRegistry.get_browser(course)
            if browser.is_place_available(agent=agent):
                logger.info("Place is available.")
                return
            else:
                logger.warn("No place available.")
            logger.info(f"Checking again in {check_interval} seconds.")
            time.sleep(check_interval)
    else:
        browser = BrowserRegistry.get_browser(course)
        if browser.is_place_available(agent=agent):
            logger.info("Place is available.")
        else:
            logger.info("No place available.")
