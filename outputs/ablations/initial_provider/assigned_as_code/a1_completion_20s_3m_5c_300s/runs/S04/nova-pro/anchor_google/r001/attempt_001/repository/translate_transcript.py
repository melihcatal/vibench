from google.cloud import translate

def translate_transcript(transcript, target_language):
    client = translate.TranslationServiceClient()
    parent = f"projects/-/locations/global"
    response = client.translate_text(
        parent=parent,
        contents=[transcript],
        target_language_code=target_language,
    )
    return response.translations[0].translated_text