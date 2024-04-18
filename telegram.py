import requests


class Telegram:
    def __init__(self, settings):
        self.settings = settings

    def send(self, message):
        url = f"https://api.telegram.org/bot{self.settings.telegram.token}/sendMessage"
        params = {"chat_id": self.settings.telegram.chat_id, "text": message}

        try:
            requests.get(url, params=params)
        except:
            print("Failed to send notification.")
