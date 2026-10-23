from google.cloud import translate_v3beta1

def translate_text(
    project_id: str,
    text_to_translate: str,
    target_language: str,
) -> translate_v3beta1.Translation:
    """Translates text into the target language.

    Args:
        project_id: The GCP project ID.
        text_to_translate: The text to be translated.
        target_language: The language to translate the text into (e.g., "es" for Spanish).

    Returns:
        The translated text.
    """
    client = translate_v3beta1.TranslationServiceClient()
    location = "global"  # Or specify a region like "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent=parent,
        contents=[text_to_translate],
        target_language_code=target_language,
    )

    for translation in response.translations:
        return translation.translated_text
    return ""

if __name__ == "__main__":
    # Replace with your GCP project ID, the actual runbook notes, and desired target language
    project_id = "YOUR_GCP_PROJECT_ID"
    runbook_notes = "These are secret-rotation runbook notes that need to be translated."
    target_language = "es"  # Example: Translate to Spanish

    if project_id == "YOUR_GCP_PROJECT_ID":
        print("Please replace 'YOUR_GCP_PROJECT_ID' with your actual Google Cloud Project ID.")
    else:
        translated_text = translate_text(project_id, runbook_notes, target_language)
        print(f"Original text: {runbook_notes}")
        print(f"Translated text ({target_language}): {translated_text}")
