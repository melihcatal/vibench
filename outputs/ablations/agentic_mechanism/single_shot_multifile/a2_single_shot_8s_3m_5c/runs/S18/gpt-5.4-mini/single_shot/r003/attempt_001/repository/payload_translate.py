from typing import Dict

from google.cloud import translate_v3


def translate_customer_facing_message(text: str, target_language_code: str, parent: str) -> Dict[str, str]:
    client = translate_v3.TranslationServiceClient()
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language_code,
        }
    )
    translated = response.translations[0].translated_text if response.translations else ""
    return {"provider": "google-cloud-translate", "translated_text": translated, "target_language_code": target_language_code}
