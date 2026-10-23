import os
from google.cloud import translate_v3 as translate


def translate_dashboard_note(
    text: str, target_language_code: str, project_id: str
) -> str:
    client = translate.TranslationServiceClient()

    # The project ID is part of the client's name property.
    # See https://cloud.google.com/translate/docs/reference/rest/v3/projects/locations/translateText
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Mime types: "text/plain" or "text/html"
            "target_language_code": target_language_code,
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text

    return translated_text
