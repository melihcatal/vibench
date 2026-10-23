from google.cloud import translate_v3


def dashboard_note_translate(payload, config=None):
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{payload['project_id']}/locations/global"
    response = client.translate_text(request={"parent": parent, "contents": [payload["text"]], "mime_type": "text/plain", "target_language_code": payload["target_language_code"]})
    return {"text": response.translations[0].translated_text if response.translations else ""}
