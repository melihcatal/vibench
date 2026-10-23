import os
import requests

OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


def check_script_safety(text: str) -> bool:
    r = requests.post(OPENAI_MODERATION_URL, headers={"Authorization": f"Bearer {OPENAI_API_KEY}"}, json={"model": "omni-moderation-latest", "input": text})
    r.raise_for_status()
    return not r.json()["results"][0]["flagged"]
