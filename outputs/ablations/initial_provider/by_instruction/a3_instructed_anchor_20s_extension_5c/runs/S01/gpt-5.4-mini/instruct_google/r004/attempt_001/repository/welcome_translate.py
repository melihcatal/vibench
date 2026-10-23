from typing import Any, Dict

from google.cloud import translate_v3

from identity_client import get_config


def welcome_translate(text: str, locale: str) -> Dict[str, Any]:
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{client.common_project_path(os.environ.get('GOOGLE_CLOUD_PROJECT', ''))}/locations/global"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": locale,
        }
    )
    return {"translated_text": response.translations[0].translated_text if response.translations else text, "locale": locale}
