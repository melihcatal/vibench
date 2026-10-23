import os
import requests


class DeepLNoteTranslator:
    def __init__(self, auth_key: str | None = None, api_base: str = "https://api-free.deepl.com/v2"):
        self.auth_key = auth_key or os.environ.get("DEEPL_AUTH_KEY")
        self.api_base = api_base

    def translate(self, text: str, target_lang: str, source_lang: str | None = None) -> str:
        if not text:
            return text
        if not self.auth_key:
            raise ValueError("DEEPL_AUTH_KEY is required")
        payload = {"text": text, "target_lang": target_lang.upper()}
        if source_lang:
            payload["source_lang"] = source_lang.upper()
        response = requests.post(
            f"{self.api_base}/translate",
            data=payload,
            headers={"Authorization": f"DeepL-Auth-Key {self.auth_key}"},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()["translations"][0]["text"]


def translate_dashboard_note(note: str, locale: str, source_lang: str | None = None) -> str:
    return DeepLNoteTranslator().translate(note, locale, source_lang=source_lang)
