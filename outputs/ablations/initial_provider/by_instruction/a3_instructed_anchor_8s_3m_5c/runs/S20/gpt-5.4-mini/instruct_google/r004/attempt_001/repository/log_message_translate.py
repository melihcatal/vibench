from google.cloud import translate_v3 as translate


def log_message_translate(text: str, target_language: str = "es") -> str:
    client = translate.TranslationServiceClient()
    parent = "projects/placeholder/locations/global"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language,
        }
    )
    return response.translations[0].translated_text
