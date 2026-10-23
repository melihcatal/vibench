from typing import Any

from google.cloud import translate_v3 as translate


def alt_text_translate(text: str, target_language: str = "es") -> str:
    client = translate.TranslationServiceClient()
    response = client.translate_text(request={"parent": "projects/placeholder/locations/global", "contents": [text], "mime_type": "text/plain", "target_language_code": target_language})
    return response.translations[0].translated_text if response.translations else ""
