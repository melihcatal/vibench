import os
from typing import List
from observability_client import ObservabilityClient
from observability_models import Translation
from google.cloud import translate_v3


def dashboard_note_translate(
    project_id: str,
    text_to_translate: List[str],
    target_language_code: str,
) -> List[Translation]:
    client = ObservabilityClient(project_id).get_translate_client()
    parent = f"projects/{project_id}/locations/global"

    translations = []
    for text in text_to_translate:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language_code,
            }
        )

        translated_text = (
            response.translations[0].translated_text if response.translations else text
        )
        translations.append(
            Translation(
                original_text=text,
                translated_text=translated_text,
                target_language=target_language_code,
            )
        )
    return translations
