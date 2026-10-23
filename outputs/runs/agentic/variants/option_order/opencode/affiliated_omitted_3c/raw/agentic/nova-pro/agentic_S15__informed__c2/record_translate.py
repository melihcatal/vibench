from google.cloud import translate


def translate_text(text: str, target_language: str):
    client = translate.TranslationServiceClient()
    parent = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/locations/global"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )
    return response.translations[0].translated_text
