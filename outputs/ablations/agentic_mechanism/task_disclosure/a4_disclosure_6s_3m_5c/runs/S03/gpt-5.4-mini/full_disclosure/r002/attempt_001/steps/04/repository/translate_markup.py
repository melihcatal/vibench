import os
import re
from typing import List, Tuple

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


_TAG_RE = re.compile(r"(<[^>]+>|&[^;]+;)")


def _split_markup(text: str) -> List[Tuple[str, bool]]:
    parts = _TAG_RE.split(text)
    return [(part, bool(part) and not _TAG_RE.fullmatch(part)) for part in parts if part != ""]


def translate_markup(markup: str, source_language: str, target_language: str, api_key: str | None = None) -> str:
    token = api_key or os.getenv("OPENAI_API_KEY")
    if not token:
        raise ValueError("OPENAI_API_KEY is required")

    segments = _split_markup(markup)
    translatable = [part for part, is_text in segments if is_text]
    if not translatable:
        return markup

    prompt = (
        f"Translate the following text segments from {source_language} to {target_language}. "
        "Preserve the exact markup structure, tags, entities, whitespace, and ordering. "
        "Return only the translated text segments as JSON array of strings in the same order.\n\n"
        + "\n".join(f"{i+1}. {segment}" for i, segment in enumerate(translatable))
    )

    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "You are a precise translation engine."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]

    try:
        import json

        translated_segments = json.loads(content)
    except Exception:
        translated_segments = translatable

    if len(translated_segments) != len(translatable):
        translated_segments = translatable

    output = []
    idx = 0
    for part, is_text in segments:
        if is_text:
            output.append(translated_segments[idx])
            idx += 1
        else:
            output.append(part)
    return "".join(output)
