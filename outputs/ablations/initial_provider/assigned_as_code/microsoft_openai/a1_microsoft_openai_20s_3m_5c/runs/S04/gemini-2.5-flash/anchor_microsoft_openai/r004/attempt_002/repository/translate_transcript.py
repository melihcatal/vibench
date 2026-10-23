import os
from google.cloud import translate_v3 as translate

def translate_transcript_segments(text_segments: List[str], target_language_code: str, project_id: str = None) -> List[str]:
    project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    translated_texts = []
    for text in text_segments:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language_code,
            }
        )
        for translation in response.translations:
            translated_texts.append(translation.translated_text)
    return translated_texts
