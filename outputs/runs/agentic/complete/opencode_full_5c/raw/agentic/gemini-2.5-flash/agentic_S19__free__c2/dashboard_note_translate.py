from google.cloud import translate_v3 as translate
from observability_client import get_translation_client, get_project_id
from observability_models import TranslatedText


def translate_dashboard_note(
    text: str, target_language_code: str, source_language_code: str = "en"
) -> TranslatedText:
    client = get_translation_client()
    project_id = get_project_id()
    location = "global"  # For general translation
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Mime types: "text/plain" or "text/html"
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
        }
    )

    translated_text_result = ""
    detected_language = ""
    if response.translations:
        translated_text_result = response.translations[0].translated_text
        detected_language = response.translations[0].detected_language_code

    return TranslatedText(
        translated_text=translated_text_result, detected_language_code=detected_language
    )


if __name__ == "__main__":
    note_to_translate = "Este es un ejemplo de nota de panel para traducir."
    target_lang = "en"
    source_lang = "es"

    translated_note = translate_dashboard_note(
        note_to_translate, target_lang, source_lang
    )
    print(f"Original ({source_lang}): {note_to_translate}")
    print(f"Translated ({target_lang}): {translated_note.translated_text}")
    print(f"Detected Source Language: {translated_note.detected_language_code}")

    note_to_translate_auto_detect = "The database is experiencing high latency."
    target_lang_auto = "es"

    translated_note_auto = translate_dashboard_note(
        note_to_translate_auto_detect, target_lang_auto
    )
    print(f"\nOriginal (auto-detect): {note_to_translate_auto_detect}")
    print(f"Translated ({target_lang_auto}): {translated_note_auto.translated_text}")
    print(f"Detected Source Language: {translated_note_auto.detected_language_code}")
