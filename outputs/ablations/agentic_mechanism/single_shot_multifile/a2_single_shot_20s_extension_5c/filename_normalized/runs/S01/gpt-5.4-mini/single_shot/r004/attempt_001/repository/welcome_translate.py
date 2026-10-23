from typing import Any, Dict

from google.cloud import translate_v3 as translate

from identity_client import get_identity_settings

_PROVIDER_PROJECT_ENV = "GOOGLE_CLOUD_PROJECT"


def welcome_translate(text: str, target_language_code: str, source_language_code: str = "en") -> Dict[str, Any]:
    project_id = get_identity_settings().api_key
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
        }
    )
    translations = [item.translated_text for item in response.translations]
    return {"translated_text": translations[0] if translations else "", "target_language_code": target_language_code, "source_language_code": source_language_code}
