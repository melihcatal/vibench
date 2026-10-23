from google.cloud import translate_v3


def log_message_translate(text, target_language, project_id=None, location="global"):
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/{location}" if project_id else None
    if parent:
        response = client.translate_text(request={"parent": parent, "contents": [text], "mime_type": "text/plain", "target_language_code": target_language})
        return response.translations[0].translated_text
    return text
