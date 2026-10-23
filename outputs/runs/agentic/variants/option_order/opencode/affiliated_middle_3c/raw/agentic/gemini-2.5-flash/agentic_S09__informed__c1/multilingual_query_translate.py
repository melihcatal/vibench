from google.cloud import translate_v2 as translate
import os


def translate_query(query: str, target_language: str = "en") -> str:
    """Translates a query to a target language using Google Cloud Translation.

    Args:
        query: The query string to translate.
        target_language: The language to translate the query into. Default is "en" (English).

    Returns:
        The translated query string.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication
    # For local development, this usually points to a service account key file.
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        print(
            "Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set. "
            "Translation might fail without proper authentication."
        )

    translate_client = translate.Client()

    response = translate_client.translate(query, target_language=target_language)

    # The response contains 'translatedText', 'detectedSourceLanguage', 'input'
    return response["translatedText"]
