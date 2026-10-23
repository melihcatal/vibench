from typing import Optional

from google.cloud import translate_v3 as translate

from identity_models import _normalize_locale


def welcome_translate(text: str, target_locale: str, *, project_id: Optional[str] = None) -> str:
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id or client.project_path.split('/')[-1]}/locations/global"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": _normalize_locale(target_locale),
        }
    )
    return response.translations[0].translated_text if response.translations else text
