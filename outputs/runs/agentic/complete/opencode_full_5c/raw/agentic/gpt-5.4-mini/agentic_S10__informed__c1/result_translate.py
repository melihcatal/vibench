import os

from google.cloud import translate_v3 as translate


def translate_result(text: str, target_language: str, project_id: str | None = None) -> str:
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id or os.getenv('GOOGLE_CLOUD_PROJECT')}/locations/global"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language,
        }
    )
    return response.translations[0].translated_text
