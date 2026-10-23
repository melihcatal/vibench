from google.cloud import translate_v3 as translate

def translate_transcript(text_segments, target_language_code, project_id):
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    translations = []
    for text in text_segments:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language_code,
            }
        )
        for translation in response.translations:
            translations.append(translation.translated_text)
    return translations
