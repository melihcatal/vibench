from google.cloud import translate

def translate_query_for_multilingual_embedding(
    query_text: str,
    target_language: str = "en"
) -> str:
    """
    Translates a query text to a target language using Google Cloud Translation API.
    This is useful before performing multilingual embedding search.

    Args:
        query_text: The original query string.
        target_language: The language code to translate the query into (e.g., "en", "fr", "es").

    Returns:
        The translated query string.
    """
    client = translate.TranslationServiceClient()

    # TODO: Replace 'your-gcp-project-id' with your actual Google Cloud Project ID
    # You might also need to set the GOOGLE_APPLICATION_CREDENTIALS environment variable.
    project_id = "your-gcp-project-id"
    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [query_text],
            "target_language_code": target_language,
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text

    return translated_text
