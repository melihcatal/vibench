from google.cloud import translate_v3


def translate_appeal_text(text: str, target_language_code: str, project_id: str) -> str:
    """Translate appeal text for review using Google Cloud Translation API."""
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )
    translated_text = response.translations[0].translated_text
    return translated_text
