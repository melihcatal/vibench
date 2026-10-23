from google.cloud import translate

def translate_caption(text, target_language_code, project_id):
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    for translation in response.translations:
        return translation.translated_text
    return None
