from google.cloud import translate_v3 as translate

def translate_text(text: str, target_language: str, project_id: str) -> str:
    """Translates text into the target language."""
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    for translation in response.translations:
        return translation.translated_text
    return ""
