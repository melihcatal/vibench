from google.cloud import translate_v3 as translate

def translate_text(text, target_language_code, project_id):
    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Mime types: "text/plain", "text/html"
            "target_language_code": target_language_code,
        }
    )

    translated_texts = []
    for translation in response.translations:
        translated_texts.append(translation.translated_text)
    return translated_texts
