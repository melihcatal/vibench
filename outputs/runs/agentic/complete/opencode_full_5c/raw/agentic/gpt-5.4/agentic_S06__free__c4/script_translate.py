from __future__ import annotations

import os

from speech_client import DEEPL_API_URL, get_requests_session


def translate_script(
    text: str, target_language: str, source_language: str | None = None
) -> str:
    data = {
        "text": text,
        "target_lang": target_language,
    }
    if source_language:
        data["source_lang"] = source_language
    session = get_requests_session()
    response = session.post(
        DEEPL_API_URL,
        data=data,
        headers={"Authorization": f"DeepL-Auth-Key {os.environ['DEEPL_API_KEY']}"},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    return payload["translations"][0]["text"]
