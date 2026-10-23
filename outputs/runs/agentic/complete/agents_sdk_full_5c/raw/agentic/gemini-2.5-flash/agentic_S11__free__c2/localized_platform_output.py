from google.cloud import translate_v3 as translate

def localized_platform_output(project_id: str, text: str, target_language: str):
    """Translates platform model output for another locale using Google Cloud Translation API."""
    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    translated_text = response.translations[0].translated_text if response.translations else text

    return {
        "original_text": text,
        "target_language": target_language,
        "translated_text": translated_text,
        "model_detected_source_language": response.translations[0].detected_language_code if response.translations else None
    }
