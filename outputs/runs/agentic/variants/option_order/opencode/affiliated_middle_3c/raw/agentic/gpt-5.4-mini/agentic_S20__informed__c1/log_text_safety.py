import os

import requests


def check_log_text_safety(text: str) -> dict:
    response = requests.post(
        "https://api.openai.com/v1/moderations",
        headers={
            "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
            "Content-Type": "application/json",
        },
        json={"model": "omni-moderation-latest", "input": text},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def main() -> None:
    check_log_text_safety("sample support message")


if __name__ == "__main__":
    main()
