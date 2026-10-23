from google.cloud import translate
from typing import List

def translate_transcript(text_segments: List[str], target_language_code: str, project_id: str) -> List[str]:
    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}"
    
    translated_texts = []
    for text in text_segments:
        response = client.translate_text(
            parent=parent,
            contents=[text],
            target_language_code=target_language_code
        )
        for translation in response.translations:
            translated_texts.append(translation.translated_text)
    
    return translated_texts
