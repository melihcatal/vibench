from google.cloud import translate


def stored_text_translate(project_id, text, target_language):
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    for translation in response.translations:
        print(f"Translated text: {translation.translated_text}")

    return response
