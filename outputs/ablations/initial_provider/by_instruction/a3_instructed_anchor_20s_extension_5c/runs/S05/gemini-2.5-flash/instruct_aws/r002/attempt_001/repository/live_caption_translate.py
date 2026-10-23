
import os
from google.cloud import translate_v3 as translate

GOOGLE_CLOUD_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
# In a real scenario, the source language might be detected or passed from STT.
# Target language would be configurable.
TARGET_LANGUAGE = os.environ.get("TARGET_LANGUAGE", "es")

async def translate_caption_chunk(text: str, project_id: str = GOOGLE_CLOUD_PROJECT_ID, target_language: str = TARGET_LANGUAGE):
    """
    Translates a caption chunk into another language using Google Cloud Translation API.
    """
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    translated_texts = []
    for translation in response.translations:
        translated_texts.append(translation.translated_text)
    
    return " ".join(translated_texts)
