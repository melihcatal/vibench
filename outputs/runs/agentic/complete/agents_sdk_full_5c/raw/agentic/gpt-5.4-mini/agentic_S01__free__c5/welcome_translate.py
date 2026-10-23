from typing import Dict

from google.cloud import translate_v3

from identity_client import build_identity_config
from identity_models import normalize_locale


class TranslationError(RuntimeError):
    pass


def welcome_translate(text: str, locale: str) -> Dict[str, str]:
    cfg = build_identity_config()
    client = translate_v3.TranslationServiceClient()
    target_language = normalize_locale(locale) or "en"
    parent = f"projects/{client.project_path.split('/')[-1]}" if hasattr(client, "project_path") else f"projects/{cfg.api_key or 'demo'}"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language,
        }
    )
    translated = response.translations[0].translated_text if response.translations else text
    return {"locale": target_language, "translated_text": translated}
