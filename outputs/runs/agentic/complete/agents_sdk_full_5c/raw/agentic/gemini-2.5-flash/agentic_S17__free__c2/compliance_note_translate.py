from google.cloud import translate_v3 as translate
from security_client import get_gcp_project_id
from security_models import TranslatedNote
from typing import List
import os

def translate_compliance_notes(project_id: str, texts: List[str], target_language_code: str, source_language_code: str = "en") -> List[TranslatedNote]:
    """Translates encryption or compliance notes using Google Cloud Translation API v3.

    Args:
        project_id: The GCP project ID.
        texts: A list of text strings to translate.
        target_language_code: The BCP-47 language code of the target language (e.g., "es" for Spanish).
        source_language_code: The BCP-47 language code of the source language (e.g., "en" for English).

    Returns:
        A list of TranslatedNote objects containing original and translated texts.
    """
    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/global"

    translated_results: List[TranslatedNote] = []

    try:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": texts,
                "mime_type": "text/plain",  # Mime types: "text/plain" or "text/html"
                "source_language_code": source_language_code,
                "target_language_code": target_language_code,
            }
        )

        for i, translation in enumerate(response.translations):
            translated_results.append(TranslatedNote(
                original_text=texts[i],
                translated_text=translation.translated_text,
                source_language=source_language_code,
                target_language=target_language_code
            ))
    except Exception as e:
        print(f"Error during translation: {e}")

    return translated_results

if __name__ == '__main__':
    PROJECT_ID = get_gcp_project_id() # Ensure GOOGLE_CLOUD_PROJECT env var is set

    notes_to_translate = [
        "Encryption key rotation completed as per policy ABC-123.",
        "La clave de cifrado se utilizó para proteger los datos del cliente.", # Spanish note
        "Audit log shows key usage for decryption operation on prod database."
    ]
    TARGET_LANG = "es" # Translate to Spanish
    SOURCE_LANG_FOR_ES = "es" # For the Spanish note, assume source is Spanish

    print(f"Translating notes to {TARGET_LANG} in project {PROJECT_ID}...")
    try:
        # Translate English notes to Spanish
        english_notes = [notes_to_translate[0], notes_to_translate[2]]
        translated_english_notes = translate_compliance_notes(PROJECT_ID, english_notes, TARGET_LANG, "en")
        for res in translated_english_notes:
            print(f"Original (en): \"{res.original_text}\"\nTranslated ({res.target_language}): \"{res.translated_text}\"\n")

        # Translate Spanish note to English
        spanish_note = [notes_to_translate[1]]
        translated_spanish_note = translate_compliance_notes(PROJECT_ID, spanish_note, "en", SOURCE_LANG_FOR_ES)
        for res in translated_spanish_note:
            print(f"Original (es): \"{res.original_text}\"\nTranslated ({res.target_language}): \"{res.translated_text}\"\n")

    except Exception as e:
        print(f"Failed to translate notes: {e}")
