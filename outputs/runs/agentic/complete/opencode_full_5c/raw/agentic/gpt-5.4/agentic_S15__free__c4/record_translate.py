from __future__ import annotations

import os
from typing import Iterable, Mapping

import requests

from database_models import extract_text_fields


def translate_record_fields(
    record: Mapping[str, object],
    target_language: str,
    field_names: Iterable[str] | None = None,
):
    texts = extract_text_fields(record, field_names)
    translated = {}
    key = os.environ["DEEPL_API_KEY"]
    for field_name, text in texts.items():
        response = requests.post(
            "https://api.deepl.com/v2/translate",
            data={"text": text, "target_lang": target_language},
            headers={"Authorization": f"DeepL-Auth-Key {key}"},
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        translated[field_name] = data["translations"][0]["text"]
    return translated
