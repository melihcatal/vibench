import os
from google.cloud import translate_v3 as translate

def translate_dashboard_note(project_id: str, text: str, target_language_code: str, source_language_code: str = "en") -> str:
    """Translates metric or dashboard notes for another locale using Google Cloud Translation.

    Args:
        project_id: Your Google Cloud project ID.
        text: The text to translate.
        target_language_code: The language code to translate the text into (e.g., "es" for Spanish).
        source_language_code: The language code of the input text (default: "en").

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()

    location = "global"  # For general purpose translation
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Mime types: "text/plain" or "text/html"
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
        }
    )

    if response.translations:
        return response.translations[0].translated_text
    else:
        return ""

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT environment variables)
    # project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    # if project_id:
    #     note_en = "CPU utilization is high, investigate potential memory leaks."
    #     target_lang = "es"
    #     print(f"Original English: {note_en}")
    #     try:
    #         translated_note = translate_dashboard_note(project_id, note_en, target_lang)
    #         print(f"Translated ({target_lang}): {translated_note}")

    #         note_fr = "L'utilisation du disque est critique, veuillez archiver les anciennes données."
    #         target_lang_en = "en"
    #         print(f"\nOriginal French: {note_fr}")
    #         translated_note_en = translate_dashboard_note(project_id, note_fr, target_lang_en, source_language_code="fr")
    #         print(f"Translated ({target_lang_en}): {translated_note_en}")

    #     except Exception as e:
    #         print(f"Error during translation: {e}")
    # else:
    #     print("GOOGLE_CLOUD_PROJECT environment variable not set. Cannot run example.")
    pass
