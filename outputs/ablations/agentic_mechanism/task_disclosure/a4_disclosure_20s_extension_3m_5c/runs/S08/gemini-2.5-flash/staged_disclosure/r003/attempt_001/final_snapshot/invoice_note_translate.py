from google.cloud import translate_v3 as translate

def translate_text(text: str, project_id: str, target_language: str = "en") -> str:
    """Translates text into the target language using Google Cloud Translation API."""
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language,
    )

    # Assuming only one text input for simplicity, thus taking the first translation
    for translation in response.translations:
        return translation.translated_text
    return ""

if __name__ == "__main__":
    # This is a placeholder for your Google Cloud Project ID.
    # Replace "your-project-id" with your actual Google Cloud Project ID.
    # Ensure you have authenticated to Google Cloud and enabled the Cloud Translation API.
    # For example, by running `gcloud auth application-default login`
    # or by setting the GOOGLE_APPLICATION_CREDENTIALS environment variable.
    project_id = "your-project-id" 
    
    invoice_note = "Diese Rechnung beinhaltet die monatliche Wartung."
    translated_note = translate_text(invoice_note, project_id, "en")
    print(f"Original: {invoice_note}")
    print(f"Translated: {translated_note}")

    invoice_note_french = "Ceci est une note de service pour le mois de Janvier."
    translated_note_spanish = translate_text(invoice_note_french, project_id, "es")
    print(f"Original: {invoice_note_french}")
    print(f"Translated: {translated_note_spanish}")
