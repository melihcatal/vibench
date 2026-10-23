import json
import os
import sys
from urllib import request


def summarize_text(text: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Summarize the user's text concisely."},
            {"role": "user", "content": text},
        ],
        "temperature": 0.2,
    }

    req = request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    return data["choices"][0]["message"]["content"].strip()


def main() -> None:
    text = sys.stdin.read()
    if not text.strip():
        raise SystemExit("No input text provided on stdin")
    print(summarize_text(text))


if __name__ == "__main__":
    main()
