from google.cloud import translate_v3 as translate

def translate_runbook_notes(text: str, target_language_code: str = "en") -> str:
    """Translates secret-rotation runbook notes using Google Cloud Translation API."""
    client = translate.TranslationServiceClient()
    project_id = "YOUR_PROJECT_ID"  # Replace with your Google Cloud Project ID
    location = "global"  # Or the region where your translation model is hosted
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        mime_type="text/plain",
        source_language_code="auto",  # Automatically detect source language
        target_language_code=target_language_code,
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    return translated_text

if __name__ == "__main__":
    sample_notes = """
    Notas del runbook de rotación de secretos:
    1. Asegúrese de que todas las aplicaciones dependientes estén actualizadas para usar el nuevo secreto.
    2. Revise los registros en busca de errores después de la rotación.
    3. Notifique a los equipos relevantes sobre el cambio.
    """
    
    # Replace "YOUR_PROJECT_ID" with your actual Google Cloud Project ID
    # Ensure you have authenticated your Google Cloud client (e.g., using `gcloud auth application-default login`)
    # before running this script.

    # Example usage: Translate to English
    english_notes = translate_runbook_notes(sample_notes, "en")
    print("Translated to English:")
    print(english_notes)

    # Example usage: Translate to Spanish
    spanish_notes = translate_runbook_notes(sample_notes, "es")
    print("\nTranslated to Spanish (re-translation for demonstration):")
    print(spanish_notes)
