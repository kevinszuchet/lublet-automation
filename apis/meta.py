import requests
import conf as CFG
from requests import HTTPError

class FacebookApi:
    def __init__(self):
        self.url = f"{CFG.meta['base_url']}/{CFG.meta['api_version']}"
        self.token = CFG.meta['token']

    def send_message(self, to, text):
        headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        template = {"name": CFG.meta['template_name'], "language": {"code": "es_AR"},
                    "components": [{"type": "body", "parameters": [{"type": "text", "text": text}]}]}
        data = {"messaging_product": "whatsapp", "to": to, "type": "template", "template": template}
        print(headers)
        print(data)
        try:
            requests.post(f"{self.url}/{CFG.meta['sender_id']}/messages", headers=headers, json=data).raise_for_status()
        except HTTPError as e:
            print("Error enviando el mensaje en WhatsApp:", e)
