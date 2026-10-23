import os
import json
from typing import Any, Dict

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def check_live_transcript_safety(transcript_text: str) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    prompt = (
        "Analyze the following live transcript text for unsafe content. "
        "Return strict JSON with keys: unsafe (boolean), category (string), "
        "confidence (number from 0 to 1), rationale (string). Transcript: "
        + transcript_text
    )

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "You are a content safety classifier."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
        },
        timeout=30,
    )
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]
    return json.loads(content)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]).strip()
    if not text:
        raise SystemExit("Provide transcript text as command-line arguments")
    print(json.dumps(check_live_transcript_safety(text), ensure_ascii=False))
