from typing import Dict
from moderation import OpenAIModeration


def moderate_profile_text(text: str) -> Dict[str, bool]:
    moderator = OpenAIModeration()
    response = moderator.moderate(text)
    return {
        "flagged": response["results"][0]["flagged"],
        "categories": response["results"][0]["categories"],
    }


class OpenAIModeration:
    def __init__(self):
        self.api_key = "sk-proj-..."
        self.url = "https://api.openai.com/v1/moderations"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def moderate(self, text: str) -> Dict:
        import requests

        payload = {"input": text}
        response = requests.post(self.url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()
