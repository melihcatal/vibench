from google.cloud import translate_v2 as translate

def translate_stored_text(
    text: str,
    target_language: str,
    project_id: str
) -> str:
    """Translates text extracted from a stored document using Google Cloud Translation API."""
    client = translate.Client(project=project_id)

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text. 
    # For this scenario, we assume a single text string.
    result = client.translate(text, target_language=target_language)

    return result["translatedText"]
