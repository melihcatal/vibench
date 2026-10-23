from google.cloud import translate_v3

from security_models import normalize_text


def compliance_note_translate(note: str, target_language: str = "en") -> str:
    client = translate_v3.TranslationServiceClient()
    parent = "projects/placeholder/locations/global"
    response = client.translate_text(request={"parent": parent, "contents": [normalize_text(note)], "target_language_code": target_language})
    return response.translations[0].translated_text if response.translations else normalize_text(note)
