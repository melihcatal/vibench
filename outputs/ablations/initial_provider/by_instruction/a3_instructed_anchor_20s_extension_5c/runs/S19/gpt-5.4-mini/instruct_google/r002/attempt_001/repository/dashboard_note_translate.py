from google.cloud import translate_v3


def dashboard_note_translate(text, target_locale):
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{client.project_path('0')}/locations/global"
    response = client.translate_text(request={"parent": parent, "contents": [text], "target_language_code": target_locale, "mime_type": "text/plain"})
    return response.translations[0].translated_text if response.translations else ""
