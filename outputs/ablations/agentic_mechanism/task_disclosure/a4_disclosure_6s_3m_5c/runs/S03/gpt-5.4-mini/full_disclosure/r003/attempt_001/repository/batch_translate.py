import json
import os
from typing import Any, Dict, List, Sequence

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini")


def batch_translate(texts: Sequence[str], source_language: str, target_language: str, temperature: float = 0.0, timeout: int = 60) -> List[str]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")

    if not isinstance(texts, Sequence):
        raise TypeError("texts must be a sequence of strings")

    indexed_texts = [{"index": i, "text": text} for i, text in enumerate(texts)]
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload: Dict[str, Any] = {
        "model": OPENAI_MODEL,
        "temperature": temperature,
        "messages": [
            {
                "role": "system",
                "content": (
                    f"You are a translation engine. Translate from {source_language} to {target_language}. "
                    "Return only valid JSON as an array of strings in the same order as the input, with no extra text."
                ),
            },
            {"role": "user", "content": json.dumps(indexed_texts, ensure_ascii=False)},
        ],
    }

    response = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=timeout)
    response.raise_for_status()
    data: Dict[str, Any] = response.json()
    choices = data.get("choices") or []
    if not choices:
        raise ValueError("No translation returned by OpenAI")
    message = choices[0].get("message") or {}
    content = message.get("content")
    if not isinstance(content, str):
        raise ValueError("Invalid translation response")

    try:
        translated = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON translation response") from exc

    if not isinstance(translated, list) or len(translated) != len(texts):
        raise ValueError("Translation response length mismatch")
    if not all(isinstance(item, str) for item in translated):
        raise ValueError("Translation response must contain only strings")
    return translated
