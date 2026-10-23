import os
from google.cloud import translate_v3 as translate

def translate_dashboard_note(text: str, target_language_code: str, project_id: str) -> str:
    """Translates metric or dashboard notes for another locale using Google Cloud Translation.

    Args:
        text: The text to translate.
        target_language_code: The BCP-47 language code of the target language (e.g., "es" for Spanish).
        project_id: The Google Cloud project ID.

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()

    # The format_glossary method is not typically used for simple text translation.
    # The parent format for text translation is projects/{project_id}/locations/global.
    # For this example, we assume 'global' location.
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language_code,
        # source_language_code='en', # Optional: if source language is known
        mime_type="text/plain", # Can be "text/html" or "text/plain"
    )

    translated_texts = [translation.translated_text for translation in response.translations]
    return translated_texts[0] if translated_texts else ""

if __name__ == '__main__':
    project = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project:
        print("Error: GOOGLE_CLOUD_PROJECT environment variable not set.")
    else:
        print("--- Translating Dashboard Notes ---")
        original_note_en = "The CPU utilization has increased significantly in the last hour."
        target_lang = "es" # Spanish
        print(f"Original (EN): {original_note_en}")
        try:
            translated_note = translate_dashboard_note(original_note_en, target_lang, project)
            print(f"Translated ({target_lang.upper()}): {translated_note}")

            original_note_fr = "L'utilisation du disque est à un niveau critique."
            target_lang_en = "en"
            print(f"\nOriginal (FR): {original_note_fr}")
            translated_note_en = translate_dashboard_note(original_note_fr, target_lang_en, project)
            print(f"Translated ({target_lang_en.upper()}): {translated_note_en}")

        except Exception as e:
            print(f"An error occurred during translation: {e}")
            print("Note: Ensure GOOGLE_APPLICATION_CREDENTIALS are set up for authentication.")
