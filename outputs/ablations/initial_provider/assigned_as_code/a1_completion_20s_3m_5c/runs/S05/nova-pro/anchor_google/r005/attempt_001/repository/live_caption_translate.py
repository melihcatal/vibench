from google.cloud import translate


def live_caption_translate(text, target_language):
    client = translate.TranslationServiceClient()
    response = client.translate_text(request={
        "parent": "projects/YOUR_PROJECT_ID/locations/global",
        "contents": [text],
        "mime_type": "text/plain",
        "target_language_code": target_language
    })
    return response.translations[0].translated_text