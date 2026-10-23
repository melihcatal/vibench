import os
from google.cloud import translate_v3 as translate

def translate_dashboard_note(text: str, target_language: str, project_id: str) -> str:
    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language,
        }
    )

    translated_texts = [translation.translated_text for translation in response.translations]
    return " ".join(translated_texts)
