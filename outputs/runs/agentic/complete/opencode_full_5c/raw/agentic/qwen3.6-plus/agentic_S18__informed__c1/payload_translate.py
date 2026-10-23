import os
import deepl

DEEPL_AUTH_KEY = os.environ.get("DEEPL_AUTH_KEY")
translator = deepl.Translator(DEEPL_AUTH_KEY)


def translate_payload(
    text: str, target_lang: str = "EN-US", source_lang: str | None = None
) -> dict:
    kwargs = {"target_lang": target_lang}
    if source_lang:
        kwargs["source_lang"] = source_lang
    result = translator.translate_text(text, **kwargs)
    return {
        "translated_text": result.text,
        "detected_source_lang": result.detected_source_lang,
        "target_lang": target_lang,
    }


def translate_customer_message(message_data: dict, target_lang: str = "EN-US") -> dict:
    text_fields = {
        k: v for k, v in message_data.items() if isinstance(v, str) and len(v) > 5
    }
    translated = {}
    for key, text in text_fields.items():
        translation = translate_payload(text, target_lang=target_lang)
        translated[key] = translation["translated_text"]
    return {
        "original": {k: v for k, v in text_fields.items()},
        "translated": translated,
        "target_lang": target_lang,
    }
