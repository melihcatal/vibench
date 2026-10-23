import os
from typing import Dict, Any
import requests


class OCRTranslator:
    def __init__(self):
        self.api_key = os.getenv("DEEPL_AUTH_KEY")
        self.base_url = "https://api-free.deepl.com/v2/translate"

    def translate_text(self, text: str, target_lang: str = "EN") -> str:
        if not self.api_key:
            raise ValueError("DEEPL_AUTH_KEY must be set")
        response = requests.post(
            self.base_url,
            data={
                "auth_key": self.api_key,
                "text": text,
                "target_lang": target_lang,
            },
        )
        response.raise_for_status()
        result = response.json()
        return result.get("translations", [{}])[0].get("text", "")