import os

from vhs_bot_ctest.notification.registry import Registry
from vhs_bot_ctest.notification.telegram import TelegramNotification


def boot_registry() -> Registry:
    notification_registry = Registry()
    telegram_bot = TelegramNotification(os.getenv("TELEGRAM_BOT_TOKEN"), os.getenv("TELEGRAM_CHAT_ID"))
    notification_registry.register(telegram_bot.name(), telegram_bot)
    return notification_registry


def choices():
    return ["telegram"]
