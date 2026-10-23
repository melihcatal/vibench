import os

import requests


def profile_moderation(text: str):
    response = requests.post("https://api.openai.com/v1/moderations", headers={"Authorization": f"Bearer {os.getenv('OPENAI_API_KEY', '')}"}, json={"model": "omni-moderation-latest", "input": text}, timeout=30)
    response.raise_for_status()
    return response.json()
