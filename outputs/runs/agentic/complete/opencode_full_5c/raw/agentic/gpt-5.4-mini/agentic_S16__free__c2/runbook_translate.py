import os

import requests


def runbook_translate(text: str, target_language: str = "es") -> str:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-5.4-mini",
            "messages": [
                {
                    "role": "system",
                    "content": f"Translate secret-rotation runbook notes into {target_language}.",
                },
                {"role": "user", "content": text},
            ],
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


if __name__ == "__main__":
    print(runbook_translate("Rotate secrets weekly."))
