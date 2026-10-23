import os
from typing import Any, Dict, Iterable, List

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def _translate_text(text: str, target_language: str, session: requests.Session) -> str:
    if not text:
        return text
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    response = session.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "Translate user-facing document fields while preserving meaning, punctuation, markdown, and placeholders.",
                },
                {
                    "role": "user",
                    "content": f"Translate the following text to {target_language}: {text}",
                },
            ],
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def _translate_value(value: Any, target_language: str, session: requests.Session) -> Any:
    if isinstance(value, str):
        return _translate_text(value, target_language, session)
    if isinstance(value, list):
        return [_translate_value(item, target_language, session) for item in value]
    if isinstance(value, dict):
        return {key: _translate_value(val, target_language, session) for key, val in value.items()}
    return value


def translate_record(record: Dict[str, Any], target_language: str) -> Dict[str, Any]:
    session = requests.Session()
    return {key: _translate_value(value, target_language, session) for key, value in record.items()}


def translate_records(records: Iterable[Dict[str, Any]], target_language: str) -> List[Dict[str, Any]]:
    session = requests.Session()
    return [{key: _translate_value(value, target_language, session) for key, value in record.items()} for record in records]
