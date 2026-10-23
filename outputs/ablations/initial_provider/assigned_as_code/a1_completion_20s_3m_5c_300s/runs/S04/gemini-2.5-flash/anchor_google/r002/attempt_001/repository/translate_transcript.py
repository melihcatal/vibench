from google.cloud import translate_v3 as translate

def translate_transcript(text, target_language_code, project_id):
    client = translate.TranslationServiceClient()
    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Mime types: text/plain, text/html
            "source_language_code": "en-US",
            "target_language_code": target_language_code,
        }
    )

    translated_text = response.translations[0].translated_text
    return {"translated_text": translated_text}
