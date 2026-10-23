import os
from typing import Optional

import requests


DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"


def translate_runbook_notes(text: str, target_lang: str = "EN-US", source_lang: Optional[str] = None) -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise RuntimeError("DEEPL_AUTH_KEY is required")

    payload = {"text": text, "target_lang": target_lang}
    if source_lang:
        payload["source_lang"] = source_lang

    response = requests.post(
        DEEPL_API_URL,
        data=payload,
        headers={"Authorization": f"DeepL-Auth-Key {auth_key}"},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return data["translations"][0]["text"]


def translate_file_notes(input_path: str, output_path: str, target_lang: str = "EN-US", source_lang: Optional[str] = None) -> None:
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()
    translated = translate_runbook_notes(text, target_lang=target_lang, source_lang=source_lang)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(translated)
