from google.cloud import translate_v2 as translate

from identity_models import compact_text, response_payload


def welcome_translate(text: str, locale: str):
    client = translate.Client()
    result = client.translate(compact_text(text), target_language=locale)
    return response_payload(
        "Cloud Translation",
        "welcome_translate",
        {
            "translated_text": result.get("translatedText"),
            "detected_source_language": result.get("detectedSourceLanguage"),
        },
    )
