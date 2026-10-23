from google.cloud import translate_v3 as translate

def localized_platform_output(text: str, target_language: str, project_id: str):
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language,
        }
    )

    translated_text = ""
    if response.translations:
        translated_text = response.translations[0].translated_text

    return {"original_text": text, "translated_text": translated_text, "target_language": target_language}
