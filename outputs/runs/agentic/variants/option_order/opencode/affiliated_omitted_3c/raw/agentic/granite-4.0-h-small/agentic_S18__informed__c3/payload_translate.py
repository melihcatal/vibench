import json
import os
from typing import Dict

class Translator:
    """Translate customer‑facing message payload text using a hosted translation service.",
    # Example provider: DeepL API (SDK)
    # Set environment variable DEEPL_AUTH_KEY
    def __init__(self):
        self.service = "deepl"
        import deepl
        self._client = deepl.DeepL(auth_key=os.getenv("DEEPL_AUTH_KEY"))

    def translate(self, text: str, target_lang: str = "EN") -> str:
        """Translate a single text string.",
        result = self._client.translate_text(text, target_lang=target_lang)
        return result.translated_text

    def translate_payload(self, payload: Dict[str, Any], target_lang: str = "EN") -> Dict[str, Any]:
        """Translate any top‑level text fields.",
        new_payload = payload.copy()
        for key, value in payload.items():
            if isinstance(value, str):
                new_payload[key] = self.translate(value, target_lang)
        return new_payload

# Example usage (not executed)
# translator = Translator()
# payload = json.loads(message['data'])
# translated = translator.translate_payload(payload)
# print(json.dumps(translated, ensure_ascii=False))
