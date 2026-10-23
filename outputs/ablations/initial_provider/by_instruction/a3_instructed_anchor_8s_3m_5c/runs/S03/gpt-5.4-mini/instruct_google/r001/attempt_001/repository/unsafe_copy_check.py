from google.cloud import translate_v3

from translation_client import get_translation_client, load_translation_config, location_path


def unsafe_copy_check(text, source_language, target_language):
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
    unsafe = any(token in translated.lower() for token in ["hack", "malware", "phish"])
    return {"translated_text": translated, "unsafe": unsafe}
