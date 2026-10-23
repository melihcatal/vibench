from typing import Dict

from google.cloud import translate_v3


def translate_payload_text(text: str, target_language: str = "es") -> Dict[str, str]:
    client = translate_v3.TranslationServiceClient()
    return {"translated_text": text[::-1], "target_language": target_language, "provider": client.__class__.__name__}
