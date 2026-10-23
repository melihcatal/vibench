from google.cloud import translate_v3 as translate

def translate_runbook_notes(text: str, project_id: str, location: str = "global",
                            source_language_code: str = "en", target_language_code: str = "es") -> str:
    """Translates text using the Google Cloud Translation API.

    Args:
        text: The text to translate.
        project_id: The Google Cloud project ID.
        location: The location of the translation service (e.g., "global", "us-central1").
        source_language_code: The language of the input text (e.g., "en" for English).
        target_language_code: The language to translate the text into (e.g., "es" for Spanish).

    Returns:
        The translated text.
    """

    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    return translated_text

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID
    YOUR_PROJECT_ID = "your-gcp-project-id"
    runbook_notes = "This runbook outlines the steps for rotating secrets. Ensure all systems are backed up before proceeding. Monitor logs for any anomalies after rotation."

    print(f"Original text: {runbook_notes}")
    translated_notes = translate_runbook_notes(runbook_notes, YOUR_PROJECT_ID, target_language_code="es")
    print(f"Translated text (Spanish): {translated_notes}")

    translated_notes_fr = translate_runbook_notes(runbook_notes, YOUR_PROJECT_ID, target_language_code="fr")
    print(f"Translated text (French): {translated_notes_fr}")
