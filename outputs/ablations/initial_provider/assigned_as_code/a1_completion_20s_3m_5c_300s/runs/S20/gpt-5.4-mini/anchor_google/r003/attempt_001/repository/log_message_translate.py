from google.cloud import translate_v3


def log_message_translate(payload, config=None):
    client = translate_v3.TranslationServiceClient()
    text = payload["text"]
    parent = payload["parent"]
    target_language = payload["target_language"]
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language,
        }
    )
    return {"translated_text": response.translations[0].translated_text}
