import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


def moderate_transcript(text: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    if not isinstance(text, str) or not text.strip():
        raise ValueError("text must be a non-empty string")

    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    prompt = (
        "Moderate this transcript for publication. Return strict JSON with keys "
        "allowed (boolean), categories (array of strings), reasons (array of strings), "
        "and cleaned_text (string). Preserve meaning while removing or redacting unsafe content.\n\n"
        f"Transcript:\n{text}"
    )

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "input": prompt,
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()

    output_text = ""
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                output_text += content.get("text", "")

    if not output_text:
        output_text = json.dumps(data)

    try:
        return json.loads(output_text)
    except json.JSONDecodeError:
        return {
            "allowed": False,
            "categories": ["unparsed_output"],
            "reasons": ["Model response was not valid JSON"],
            "cleaned_text": "",
            "raw_response": output_text,
        }


if __name__ == "__main__":
    import sys

    transcript = sys.stdin.read()
    result = moderate_transcript(transcript)
    print(json.dumps(result, ensure_ascii=False, indent=2))
