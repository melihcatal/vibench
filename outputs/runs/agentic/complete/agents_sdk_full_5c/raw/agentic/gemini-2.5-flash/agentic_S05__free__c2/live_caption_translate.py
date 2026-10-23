from google.cloud import translate_v3 as translate

def translate_caption_chunk(
    text_content: str,
    target_language_code: str,
    project_id: str
) -> str:
    """
    Translates a live caption chunk into another language using Google Cloud Translation.
    """
    client = translate.TranslationServiceClient()
    
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text_content],
            "target_language_code": target_language_code,
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    
    return translated_text
