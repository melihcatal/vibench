import os
import requests

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")


def moderation_summary(text):
    url = "https://api.anthropic.com/v1/complete"
    headers = {"Content-Type": "application/json", "x-api-key": ANTHROPIC_API_KEY}
    payload = {
        "prompt": f"Summarize the following text: {text}",
        "model": "claude-v1",
        "max_tokens_to_sample": 100,
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json().get("completion", "")
