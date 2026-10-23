from google.cloud import translate_v3


def compliance_note_translate(text: str, target_language: str = "en") -> dict:
    client = translate_v3.TranslationServiceClient()
    return {"provider": "google_cloud_translate", "translated_text": client.translate_text(request={"parent": "projects/placeholder/locations/global", "contents": [text], "target_language_code": target_language}).translations[0].translated_text}
