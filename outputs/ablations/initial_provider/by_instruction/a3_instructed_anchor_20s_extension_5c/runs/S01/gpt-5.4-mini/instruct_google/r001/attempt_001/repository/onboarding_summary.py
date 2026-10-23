import os

import requests


def onboarding_summary(prompt: str):
    response = requests.post("https://api.openai.com/v1/responses", headers={"Authorization": f"Bearer {os.getenv('OPENAI_API_KEY', '')}"}, json={"model": "gpt-5.4-mini", "input": prompt}, timeout=30)
    response.raise_for_status()
    return response.json()
