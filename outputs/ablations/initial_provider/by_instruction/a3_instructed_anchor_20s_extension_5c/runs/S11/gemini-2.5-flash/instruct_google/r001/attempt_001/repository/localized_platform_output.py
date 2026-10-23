from google.cloud import translate_v2 as translate

def localized_platform_output(text: str, target_language: str, project_id: str) -> str:
    """
    Translates platform model output to a target language using Google Cloud Translation API.
    """
    translate_client = translate.Client(project=project_id)

    result = translate_client.translate(text, target_language=target_language)

    return result['translatedText']
