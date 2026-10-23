from google.cloud import translate_v3beta1 as translate

def translate_query(text: str, target_language: str) -> str:
    """Translates a given text to the target language using Google Cloud Translation API.

    Args:
        text: The text to translate.
        target_language: The language to translate the text into (e.g., "es" for Spanish).

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/your-gcp-project-id"  # Replace with your GCP project ID

    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language,
        mime_type="text/plain",
    )

    return response.translations[0].translated_text
