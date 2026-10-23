from google.cloud import translate_v3 as translate

def translate_alt_text(text: str, target_language: str, project_id: str) -> str:
    """Translates text into the target language using Google Cloud Translation API."""
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    translated_text = response.translations[0].translated_text
    return translated_text

