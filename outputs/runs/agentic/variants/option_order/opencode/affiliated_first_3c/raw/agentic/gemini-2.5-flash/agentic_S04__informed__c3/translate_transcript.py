import os
from google.cloud import translate


def translate_text_segments(
    text_segments: list[str], target_language: str
) -> list[str]:
    """
    Translates completed transcript segments using Google Cloud Translation.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

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
