from __future__ import annotations

from typing import Any, Dict

from deepl import DeepLClient

DEEPL_TARGET_DEFAULT = "EN-US"
DEEPL_PROVIDER = "api-free.deepl.com"


class InvoiceNoteTranslator:
    def __init__(self, auth_key: str | None = None):
        import os
        self.client = DeepLClient(auth_key or os.getenv("DEEPL_AUTH_KEY", ""))

    def translate(self, text: str, target_lang: str = DEEPL_TARGET_DEFAULT, source_lang: str | None = None) -> Dict[str, Any]:
        result = self.client.translate_text(text, target_lang=target_lang, source_lang=source_lang)
        return {
            "translated_text": result.text,
            "detected_source_language": getattr(result, "detected_source_lang", source_lang),
            "target_language": target_lang,
            "provider": "deepl",
            "endpoint": DEEPL_PROVIDER,
        }
