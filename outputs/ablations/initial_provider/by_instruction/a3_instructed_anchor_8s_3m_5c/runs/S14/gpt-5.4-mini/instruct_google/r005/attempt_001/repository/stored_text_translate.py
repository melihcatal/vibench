from google.cloud import translate_v3

from storage_models import TranslationResult


def stored_text_translate(text: str, project_id: str, location: str, target_language: str, source_language: str = "") -> TranslationResult:
    client = translate_v3.TranslationServiceClient()
    parent = client.location_path(project_id, location)
    response = client.translate_text(request={"parent": parent, "contents": [text], "mime_type": "text/plain", "target_language_code": target_language, "source_language_code": source_language or None})
    translated = response.translations[0].translated_text if response.translations else ""
    source = response.translations[0].detected_language_code if response.translations else source_language or None
    return TranslationResult(source_language=source, target_language=target_language, text=translated)
