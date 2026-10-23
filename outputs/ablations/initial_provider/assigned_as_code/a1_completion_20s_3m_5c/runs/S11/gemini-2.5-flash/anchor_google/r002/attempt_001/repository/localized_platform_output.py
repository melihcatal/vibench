from google.cloud import translate_v3 as translate

def localized_platform_output(text_content: str, target_language_code: str, project_id: str):
    client = translate.TranslationServiceClient()
    location = "global"  # Translation API is global
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text_content],
            "target_language_code": target_language_code,
        }
    )

    translations = []
    for translation in response.translations:
        translations.append({"translated_text": translation.translated_text, "detected_language_code": translation.detected_language_code})
    
    return {"translations": translations}
