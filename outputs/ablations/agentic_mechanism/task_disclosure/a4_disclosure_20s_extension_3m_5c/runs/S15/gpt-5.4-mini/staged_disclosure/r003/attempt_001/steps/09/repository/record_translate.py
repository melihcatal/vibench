import os
from typing import Any, Dict

import requests


class DeepLTranslator:
    def __init__(self, auth_key: str | None = None, base_url: str = "https://api-free.deepl.com/v2/translate"):
        self.auth_key = auth_key or os.getenv("DEEPL_AUTH_KEY")
        self.base_url = base_url

    def translate_text(self, text: str, target_lang: str) -> str:
        if not text:
            return text
        if not self.auth_key:
            raise RuntimeError("DEEPL_AUTH_KEY is required")
        response = requests.post(
            self.base_url,
            data={"auth_key": self.auth_key, "text": text, "target_lang": target_lang},
            timeout=30,
        )
        response.raise_for_status()
        payload = response.json()
        translations = payload.get("translations") or []
        if not translations:
            raise RuntimeError("DeepL translation response missing translations")
        return translations[0].get("text", text)


def translate_record_fields(record: Dict[str, Any], target_lang: str = "EN") -> Dict[str, Any]:
    translator = DeepLTranslator()
    translated = dict(record)
    for field in ("title", "summary", "description", "body", "content"):
        value = translated.get(field)
        if isinstance(value, str) and value.strip():
            translated[field] = translator.translate_text(value, target_lang)
    return translated


def translate_document_fields(record: Dict[str, Any], target_lang: str = "EN") -> Dict[str, Any]:
    return translate_record_fields(record, target_lang)
