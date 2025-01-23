import os
import json
import requests

class EATSSlackNotice:
    
    def __init__(self, channel):
        self.channel = channel
        self.url = "https://slack.com/api/chat.postMessage"
        self.token = os.environ.get("token")
        self.token_type = "Bearer"
    
    def send_message(self, message) -> None:
        headers={"Authorization": f"{self.token_type} {self.token} "}
        try:
            response = requests.get(
                            self.url,
                            headers=headers,
                            params={'channel': self.channel, 'text': message}
                            )
            print(response.status_code)
            data = json.loads(response.text)
            if data.get("ok") != True:
                print(data)
        except requests.exceptions.Timeout as errd:
            print("SlackNotice Timeout Error")
        except requests.exceptions.ConnectionError as errc:
            print("SlackNotice Connection Error")
        except requests.exceptions.HTTPError as errb:
            print("SlackNotice Http Error")
        except requests.exceptions.RequestException as erra:
            print("SlackNotice AnyException")