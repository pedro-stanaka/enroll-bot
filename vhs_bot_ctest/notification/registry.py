from vhs_bot_ctest.notification.base import BaseNotification


class Registry:
    def __init__(self):
        self._registry: dict[str, BaseNotification] = {}

    def register(self, notification_type: str, notification) -> None:
        self._registry[notification_type] = notification

    def get_notification(self, notification_type) -> BaseNotification | None:
        return self._registry.get(notification_type)

    def get_names(self) -> list[str]:
        return self._registry.keys()
