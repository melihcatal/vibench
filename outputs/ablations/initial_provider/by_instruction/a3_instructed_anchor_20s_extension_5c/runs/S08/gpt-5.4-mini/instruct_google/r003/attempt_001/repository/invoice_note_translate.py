from typing import Any, Dict

from google.cloud import translate_v3


def invoice_note_translate(text: str, target_language: str = "en") -> Dict[str, Any]:
    client = translate_v3.TranslationServiceClient()
    parent = "projects/"
    response = client.translate_text(request={"parent": parent, "contents": [text], "target_language_code": target_language})
    translation = response.translations[0].translated_text if response.translations else text
    return {"translated_text": translation, "provider": "google_translate_v3"}
