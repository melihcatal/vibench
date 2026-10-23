import json
import os
import requests


def main():
    api_key = os.environ["OPENAI_API_KEY"]
    text = os.getenv("LOG_TEXT", "")
    response = requests.post(
        "https://api.openai.com/v1/moderations",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": "omni-moderation-latest", "input": text},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    print(json.dumps(main(), default=str))