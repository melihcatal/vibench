from google.cloud import translate_v2 as translate

def localized_platform_output(text_content: str, target_language: str, project_id: str):
    """Translates platform model output to another locale using Google Cloud Translation API."""
    translate_client = translate.Client(project=project_id)

    # Target can be a language code (e.g., "fr" for French, "es" for Spanish, "en" for English)
    response = translate_client.translate(text_content, target_language=target_language)

    return {
        "translated_text": response["translatedText"],
        "original_text": response["input"],
        "detected_source_language": response["detectedSourceLanguage"],
    }
