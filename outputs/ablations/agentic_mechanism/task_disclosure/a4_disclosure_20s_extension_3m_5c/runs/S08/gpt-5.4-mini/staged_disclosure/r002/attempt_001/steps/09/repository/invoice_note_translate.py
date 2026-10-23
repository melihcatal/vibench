import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


def _read_input(source: Optional[str]) -> str:
    if source and os.path.isfile(source):
        with open(source, "r", encoding="utf-8") as f:
            return f.read()
    if source:
        return source
    return os.environ.get("INVOICE_NOTE_TEXT", "")


def _build_prompt(text: str, target_language: str) -> str:
    return (
        "Translate the invoice note, description, or memo below into the target language. "
        "Preserve meaning, numbers, dates, codes, product names, and formatting. "
        "If the input already appears in the target language, return it unchanged. "
        "Return strict JSON only with keys translated_text and target_language.\n\n"
        f"Target language: {target_language}\n"
        f"Invoice note:\n{text}"
    )


def _parse_response(data: Dict[str, Any]) -> str:
    output_text = ""
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") == "output_text":
                output_text += content.get("text", "")
    if not output_text:
        raise ValueError("OpenAI response did not contain output text")
    try:
        parsed = json.loads(output_text)
    except json.JSONDecodeError:
        start = output_text.find("{")
        end = output_text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            return output_text.strip()
        parsed = json.loads(output_text[start : end + 1])
    if isinstance(parsed, dict):
        translated = parsed.get("translated_text")
        if translated:
            return str(translated).strip()
    return output_text.strip()


def translate_invoice_note(text: str, target_language: str = "English", api_key: Optional[str] = None) -> str:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    payload = {
        "model": OPENAI_MODEL,
        "input": _build_prompt(text, target_language),
        "temperature": 0,
    }
    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    return _parse_response(response.json())


def main() -> None:
    import sys

    source = sys.argv[1] if len(sys.argv) > 1 else None
    target_language = sys.argv[2] if len(sys.argv) > 2 else os.environ.get("TARGET_LANGUAGE", "English")
    text = _read_input(source)
    print(translate_invoice_note(text, target_language=target_language))


if __name__ == "__main__":
    main()
