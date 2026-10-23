import json
import os
import sys
from typing import Any, Dict, List

import requests


OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def _extract_text(payload: Any) -> str:
    if isinstance(payload, str):
        return payload.strip()
    if isinstance(payload, dict):
        for key in ("text", "note", "description", "content", "invoice_note"):
            value = payload.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        for key in ("notes", "descriptions", "items"):
            value = payload.get(key)
            if isinstance(value, list):
                parts = []
                for item in value:
                    text = _extract_text(item)
                    if text:
                        parts.append(text)
                if parts:
                    return "\n".join(parts)
    if isinstance(payload, list):
        parts = []
        for item in payload:
            text = _extract_text(item)
            if text:
                parts.append(text)
        return "\n".join(parts)
    return str(payload).strip()


def translate_invoice_note(text: str, target_language: str = "en") -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    prompt = (
        "Translate the following invoice note or description into "
        f"{target_language}. Preserve amounts, dates, IDs, names, and formatting. "
        "Return only the translated text.\n\n"
        f"{text}"
    )

    response = requests.post(
        OPENAI_CHAT_COMPLETIONS_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "You translate invoice notes accurately and concisely."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def main() -> None:
    raw_input = sys.stdin.read().strip()
    if not raw_input:
        raise SystemExit(1)

    try:
        payload = json.loads(raw_input)
    except json.JSONDecodeError:
        payload = raw_input

    target_language = "en"
    text = payload
    if isinstance(payload, dict):
        target_language = str(payload.get("target_language", target_language))
        text = payload.get("text") or payload.get("note") or payload.get("description") or payload

    extracted = _extract_text(text)
    if not extracted:
        raise SystemExit(1)

    result = translate_invoice_note(extracted, target_language=target_language)
    sys.stdout.write(result)


if __name__ == "__main__":
    main()
