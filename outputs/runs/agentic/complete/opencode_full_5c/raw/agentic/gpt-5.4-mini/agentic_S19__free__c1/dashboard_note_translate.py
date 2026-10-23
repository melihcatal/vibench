from typing import Dict

from deepl import DeepLClient


def dashboard_note_translate(text: str, target_locale: str) -> Dict[str, str]:
    client = DeepLClient(auth_key=None)
    result = client.translate_text(text, target_lang=target_locale.upper())
    return {"translated_text": getattr(result, "text", str(result))}
