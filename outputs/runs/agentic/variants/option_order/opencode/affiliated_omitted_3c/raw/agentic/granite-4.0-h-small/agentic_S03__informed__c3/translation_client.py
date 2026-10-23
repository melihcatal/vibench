import os
from typing import Dict, Any
from translation_client import TranslationClient


class TranslationClient:
    """Local helper to configure provider credentials and expose high‑level translation methods."""

    def __init__(self):
        # Example: read env vars for a chosen provider (replace with real config logic)
        self.api_key = os.getenv("DEEPL_AUTH_KEY")
        self.service = "DeepL"  # identifier for code‑readability

    def translate(self, text: str, src: str, tgt: str) -> Dict[str, Any]:
        """Single‑string translation via DeepL SDK."""
        from deepl import DeepL

        deepl = DeepL(auth_key=self.api_key)
        result = deepl.translate_text(text, target_lang=tgt)
        return {"translatedText": result["text"]}

    def translate_batch(
        self, texts: list[str], src: str, tgt: str
    ) -> list[Dict[str, Any]]:
        from deepl import DeepL

        deepl = DeepL(auth_key=self.api_key)
        results = deepl.translate_text(texts, target_lang=tgt)
        return [{"translatedText": r["text"]} for r in results]
