from google.cloud import translate_v3 as translate
import os
from typing import List

def translate_text_with_google_cloud(project_id: str, texts: List[str], target_language: str, source_language: str = "en") -> List[str]:
    """
    Translates a list of texts to a target language using Google Cloud Translation API.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    translated_texts = []
    for text in texts:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "mime_type": "text/plain",
                "source_language_code": source_language,
                "target_language_code": target_language,
            }
        )
        for translation in response.translations:
            translated_texts.append(translation.translated_text)
    return translated_texts

def translate_runbook_notes(project_id: str, notes: List[str], target_language: str, source_language: str = "en") -> List[str]:
    """
    Translates secret-rotation runbook notes to a target language.
    """
    if not notes:
        return []
    return translate_text_with_google_cloud(project_id, notes, target_language, source_language)

if __name__ == "__main__":
    # Example usage:
    # project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    # example_notes = [
    #     "Update the database password in the configuration file.",
    #     "Check the application logs after rotation."
    # ]
    # target_lang = "es"
    # if project_id:
    #     translated_notes = translate_runbook_notes(project_id, example_notes, target_lang)
    #     for i, translated_note in enumerate(translated_notes):
    #         print(f"Original: '{example_notes[i]}' -> Translated ({target_lang}): '{translated_note}'")
    # else:
    #     print("Please set GOOGLE_CLOUD_PROJECT environment variable.")
    pass
