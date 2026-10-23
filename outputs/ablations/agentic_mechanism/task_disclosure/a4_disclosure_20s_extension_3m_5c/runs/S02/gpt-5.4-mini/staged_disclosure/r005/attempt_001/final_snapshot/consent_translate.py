import os
from typing import Dict, Iterable, List, Optional

import requests


DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"


def _chunk_text(text: str, max_chars: int = 3500) -> List[str]:
    if len(text) <= max_chars:
        return [text]
    parts = []
    current = []
    current_len = 0
    for paragraph in text.split("\n"):
        add_len = len(paragraph) + (1 if current else 0)
        if current_len + add_len > max_chars and current:
            parts.append("\n".join(current))
            current = [paragraph]
            current_len = len(paragraph)
        else:
            current.append(paragraph)
            current_len += add_len
    if current:
        parts.append("\n".join(current))
    return parts


def translate_consent_copy(text: str, target_lang: str, source_lang: Optional[str] = None) -> str:
    api_key = os.environ.get("DEEPL_AUTH_KEY")
    if not api_key:
        raise RuntimeError("DEEPL_AUTH_KEY is required")

    headers = {"Authorization": f"DeepL-Auth-Key {api_key}"}
    translated_chunks: List[str] = []

    for chunk in _chunk_text(text):
        payload: Dict[str, str] = {"text": chunk, "target_lang": target_lang}
        if source_lang:
            payload["source_lang"] = source_lang
        response = requests.post(DEEPL_API_URL, headers=headers, data=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        translations = data.get("translations", [])
        if not translations:
            raise RuntimeError("DeepL returned no translations")
        translated_chunks.append(translations[0]["text"])

    return "".join(translated_chunks)


def translate_consent_items(items: Iterable[str], target_lang: str, source_lang: Optional[str] = None) -> List[str]:
    return [translate_consent_copy(item, target_lang, source_lang) for item in items]


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        raise SystemExit("usage: consent_translate.py TARGET_LANG TEXT [SOURCE_LANG]")
    target = sys.argv[1]
    source = sys.argv[3] if len(sys.argv) > 3 else None
    print(translate_consent_copy(sys.argv[2], target, source))
