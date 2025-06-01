# main.py
import time
import threading
from http.server import HTTPServer

import click
import structlog
from dotenv import load_dotenv
from prometheus_client import Counter, start_http_server

from vhs_bot_ctest import notification
from vhs_bot_ctest.browse.registry import BrowserRegistry
from vhs_bot_ctest.logging import configure_logging
from vhs_bot_ctest.browse.base import NetworkError, ElementNotFoundError

FIVE_MINUTES_SECONDS = 5 * 60

# Define Prometheus metrics
TOTAL_CHECKS = Counter('vhs_bot_total_checks', 'Total number of availability checks')
SUCCESSFUL_CHECKS = Counter('vhs_bot_successful_checks', 'Number of successful availability checks')
NETWORK_ERRORS = Counter('vhs_bot_network_errors', 'Number of network errors encountered')

@click.command()
@click.option(
    "--course",
    default=None,
    required=True,
    help="Course name.",
    type=click.Choice(BrowserRegistry.get_names(), case_sensitive=True),
)
@click.option(
    "-n",
    "--notification",
    "notification_type",
    default="",
    required=False,
    help="Method used for notification about vacancies.",
    type=click.Choice(notification.choices(), case_sensitive=True),
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
@click.option(
    "--continue-after-success",
    default=False,
    help="Continue checking even after finding an available place.",
    is_flag=True,
)
@click.option(
    "--metrics-port",
    default=8000,
    help="Port for Prometheus metrics endpoint.",
)
def main(
    course,
    notification_type=None,
    agent=None,
    watch=False,
    check_interval=60,
    continue_after_success=False,
    metrics_port=8000,
):
    """Check the availability of free slots for courses and tests at VHS schools."""
    # Configure logging
    configure_logging()

    # Start Prometheus metrics server
    start_http_server(metrics_port)
    logger = structlog.get_logger(course=course, notification_type=notification_type)
    logger.info(f"Started metrics server on port {metrics_port}")

    # TODO: introduce a watch mode
    # TODO: notify the user about the availability of a place, e.g. via telegram (configure using ENV vars)
    #    package telegram-notification seems easy to use
    # TODO: allow overriding browser config in playwright via ENV vars or CLI args
    load_dotenv()
    registry = notification.boot_registry()
    if agent:
        logger = logger.bind(agent=agent)

    def check_availability():
        browser = BrowserRegistry.get_browser(course)
        TOTAL_CHECKS.inc()

        try:
            if browser.is_place_available(agent=agent):
                SUCCESSFUL_CHECKS.inc()
                logger.info("Place is available.")
                notification_sender = registry.get_notification(notification_type)
                if notification_sender is not None:
                    logger.info("Sending notification.", notification_type=notification_type)
                    res = notification_sender.send(f"Place is available for {browser.human_name()}.\nBook here: {browser.site}")
                    if not res:
                        logger.error("Failed to send notification.")
                return True
            logger.warn("No place available.")
            return False
        except NetworkError as e:
            NETWORK_ERRORS.inc()
            logger.error("Network error occurred", error=str(e))
            return False
        except ElementNotFoundError as e:
            logger.error("Element not found", error=str(e))
            return False
        except Exception as e:
            logger.error("Unexpected error occurred", error=str(e))
            return False

    if watch:
        while True:
            found = check_availability()
            if found and not continue_after_success:
                return
            logger.info(f"Checking again in {check_interval} seconds.")
            time.sleep(check_interval)
    else:
        check_availability()
