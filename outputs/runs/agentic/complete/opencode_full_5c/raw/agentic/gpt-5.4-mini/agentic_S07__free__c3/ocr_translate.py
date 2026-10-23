from google.cloud import translate_v3


def ocr_translate(text, target_language="en"):
    client = translate_v3.TranslationServiceClient()
    parent = (
        f"projects/{__import__('os').getenv('GOOGLE_CLOUD_PROJECT')}/locations/global"
    )
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language,
        }
    )
    return response.translations[0].translated_text if response.translations else ""
