import os
from typing import List
from google.cloud import translate_v3 as translation

def translate_segments(text_segments: List[str], target_language_code: str, project_id: str) -> List[str]:
    client = translation.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": text_segments,
            "target_language_code": target_language_code,
        }
    )

    translated_texts = [translation.translated_text for translation in response.translations]
    return translated_texts