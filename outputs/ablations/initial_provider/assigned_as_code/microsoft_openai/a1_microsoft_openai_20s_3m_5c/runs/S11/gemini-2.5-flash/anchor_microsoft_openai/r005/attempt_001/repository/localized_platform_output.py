from google.cloud import translate_v2 as translate

def localized_platform_output(text_output: str, target_language: str, project_id: str):
    """
    Translates platform model output to another locale using Google Cloud Translation.
    """
    translate_client = translate.Client(project=project_id)

    if isinstance(text_output, bytes):
        text_output = text_output.decode("utf-8")

    result = translate_client.translate(text_output, target_language=target_language)

    return {
        "translated_text": result["translatedText"],
        "original_text": result["input"],
        "detected_source_language": result["detectedSourceLanguage"],
    }
