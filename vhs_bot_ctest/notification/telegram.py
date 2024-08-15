import requests

from vhs_bot_ctest.notification.base import BaseNotification


class MissingTokenOrChatIdError(ValueError):
    pass


class TelegramNotification(BaseNotification):
    TELEGRAM_URL_TEMPLATE = "https://api.telegram.org/bot{}/sendMessage"

    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id

    def send(self, message) -> bool:
        self.__validate_token_and_chat_id()
        url = self.TELEGRAM_URL_TEMPLATE.format(self.token)
        resp = requests.post(url, data={"chat_id": self.chat_id, "text": message})
        return resp.status_code == 200

    def name(self) -> str:
        return "telegram"

    def __validate_token_and_chat_id(self):
        if not self.token or not self.chat_id:
            raise MissingTokenOrChatIdError("TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables must be set")
