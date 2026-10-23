import os
import requests

API_KEY = os.getenv("TEXT_SAFETY_API_KEY")
API_URL = "https://api.textsafety.com/moderate"


def get_client():
    return TextSafetyClient()


class TextSafetyClient:
    def moderate_text(self, text):
        headers = {"Authorization": f"Bearer {API_KEY}"}
        payload = {"text": text}
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
