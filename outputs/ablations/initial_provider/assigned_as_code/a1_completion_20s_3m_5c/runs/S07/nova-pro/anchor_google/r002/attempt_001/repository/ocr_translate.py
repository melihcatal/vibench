from google.cloud import translate


def translate_text(text, target_language):
    client = translate.TranslationServiceClient()
    parent = f"projects/YOUR_PROJECT_ID/locations/global"
    response = client.translate_text(request={
        "parent": parent,
        "contents": [text],
        "mime_type": "text/plain",
        "target_language_code": target_language
    })
    return response.translations[0].translated_text