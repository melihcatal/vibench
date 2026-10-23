from google.cloud import translate_v3 as translate

def translate_text(project_id: str, text: str, target_language_code: str = "en") -> str:
    """Translates a given text using Google Cloud Translation."""
    client = translate.TranslationServiceClient()
    location = "global"  # Or specify a region like "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language_code,
        mime_type="text/plain",
    )

    translations = [translation.translated_text for translation in response.translations]
    return " ".join(translations)

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID
    # For example, you can get it from the GOOGLE_CLOUD_PROJECT environment variable
    # or pass it as an argument.
    project_id = "YOUR_GOOGLE_CLOUD_PROJECT_ID" 

    # Example usage:
    runbook_notes = "Las notas del runbook de rotación de secretos deben traducirse al inglés."
    translated_notes = translate_text(project_id, runbook_notes, "en")
    print(f"Original notes: {runbook_notes}")
    print(f"Translated notes: {translated_notes}")
