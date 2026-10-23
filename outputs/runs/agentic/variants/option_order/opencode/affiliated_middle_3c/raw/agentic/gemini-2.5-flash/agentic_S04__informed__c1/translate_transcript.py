import os
from typing import List

from google.cloud import translate_v3 as translate


def translate_segments(
    text_segments: List[str], target_language: str, project_id: str = None
) -> List[str]:
    """Translates a list of text segments using Google Cloud Translation."""
    if project_id is None:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError(
            "Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT environment variable not set."
        )

    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    translated_texts = []
    for text in text_segments:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language,
            }
        )
        for translation in response.translations:
            translated_texts.append(translation.translated_text)
    return translated_texts
