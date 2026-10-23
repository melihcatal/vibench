from google.cloud import translate_v3

from translation_client import get_translation_client, load_translation_config, location_path


def quality_summary(text, source_language, target_language):
    config = load_translation_config()
    client = get_translation_client()
    response = client.translate_text(
        request={
            "parent": location_path(config),
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": source_language,
            "target_language_code": target_language,
        }
    )
    translated = response.translations[0].translated_text
    issues = []
    if translated == text:
        issues.append("unchanged")
    return {"translated_text": translated, "issues": issues}
