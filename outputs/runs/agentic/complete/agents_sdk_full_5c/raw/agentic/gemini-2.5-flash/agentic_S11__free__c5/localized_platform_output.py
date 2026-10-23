from google.cloud import translate_v2 as translate

def translate_platform_output(project_id: str, text: str, target_language: str) -> str:
    """Translates platform model output to another locale using Google Cloud Translation API."""
    translate_client = translate.Client(project=project_id)

    # Text can also be a list of strings, in which case a list of translations is returned.
    # We assume a single string for simplicity here.
    result = translate_client.translate(
        text, target_language=target_language
    )
    
    # The result contains 'translatedText', 'detectedSourceLanguage', and 'input'
    return result['translatedText']
