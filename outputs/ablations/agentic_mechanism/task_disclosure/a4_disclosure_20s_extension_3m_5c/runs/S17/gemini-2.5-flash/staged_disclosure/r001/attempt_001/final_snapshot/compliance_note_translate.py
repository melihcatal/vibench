from google.cloud import translate_v3 as translate

def translate_text(
    text: str,
    project_id: str,
    target_language: str = "en",
    location: str = "global",
) -> str:
    """Translates text into the target language.

    Args:
        text: The text to translate.
        project_id: Your Google Cloud Project ID.
        target_language: The language to translate the text into (e.g., "en" for English).
        location: The location of the translation service (e.g., "global").

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    return translated_text

if __name__ == "__main__":
    # Replace with your actual Google Cloud Project ID
    YOUR_PROJECT_ID = "your-gcp-project-id"
    note_to_translate = "Este documento contiene información confidencial sobre el cifrado."
    
    # Example usage: Translate to English
    translated_note = translate_text(
        text=note_to_translate,
        project_id=YOUR_PROJECT_ID,
        target_language="en",
    )
    print(f"Original: {note_to_translate}")
    print(f"Translated (en): {translated_note}")

    # Example usage: Translate to French
    translated_note_fr = translate_text(
        text=note_to_translate,
        project_id=YOUR_PROJECT_ID,
        target_language="fr",
    )
    print(f"Translated (fr): {translated_note_fr}")
