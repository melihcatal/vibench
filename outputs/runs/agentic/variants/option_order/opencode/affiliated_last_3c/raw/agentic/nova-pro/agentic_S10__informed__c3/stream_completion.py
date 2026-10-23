import os
import requests

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")


def stream_completion(prompt):
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "mistral-large-latest",
        "messages": [{"role": "user", "content": prompt}],
        "stream": True,
    }
    response = requests.post(
        "https://api.mistral.ai/v1/chat/completions",
        headers=headers,
        json=data,
        stream=True,
    )
    for line in response.iter_lines():
        if line:
            yield line.decode("utf-8")
