# [LATER-STEP] result_translate.py

import os
import requests

class DeeplTranslator:
    """Wrapper around DeepL API for translating model output."""
    BASE_URL = "https://api.deepl.com/v2/translate"
    API_KEY = os.getenv("DEEPL_AUTH_KEY")
    if not API_KEY:
        raise RuntimeError("Set DEEPL_AUTH_KEY environment variable")

    @staticmethod
    def translate(text: str, target_lang: str = "EN") -> str:
        payload = {
            "auth_key": DeeplTranslator.API_KEY,
            "text": text,
            "target_lang": target_lang
        }
        resp = requests.post(DeeplTranslator.BASE_URL, data=payload)
        resp.raise_for_status()
        data = resp.json()
        translations = data.get("translations", [])
        if not translations:
            raise ValueError("Translation failed")
        return translations[0]["text"]
