from google.cloud import translate_v3 as translate
from typing import List

def translate_text_segments(text_segments: List[str], target_language_code: str, project_id: str) -> List[str]:
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    translated_texts = []
    for text in text_segments:
        response = client.translate_text(
            parent=parent,
            contents=[text],
            mime_type="text/plain",  # Mime types: text/plain, text/html
            source_language_code="en-US", # Assuming source is English from transcription
            target_language_code=target_language_code,
        )

        for translation in response.translations:
            translated_texts.append(translation.translated_text)
    return translated_texts
