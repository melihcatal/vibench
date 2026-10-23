import json
import os
from typing import Optional
import deepl


DEEPL_AUTH_KEY = os.environ.get("DEEPL_AUTH_KEY", "")


def translate_message_payload(
    text: str,
    target_language: str = "EN",
    source_language: Optional[str] = None,
) -> dict:
    if not DEEPL_AUTH_KEY:
        return {
            "success": False,
            "error": "DEEPL_AUTH_KEY environment variable is not set",
            "translated_text": text,
        }

    try:
        translator = deepl.Translator(DEEPL_AUTH_KEY)
        translate_kwargs = {
            "target_lang": target_language.upper(),
        }
        if source_language:
            translate_kwargs["source_lang"] = source_language.upper()

        result = translator.translate_text(text, **translate_kwargs)

        return {
            "success": True,
            "translated_text": result.text,
            "detected_source_language": result.detected_source_lang,
            "target_language": target_language,
            "service": "DeepL API",
        }
    except deepl.DeepLException as exc:
        return {
            "success": False,
            "error": str(exc),
            "translated_text": text,
        }


def main():
    sample_text = os.environ.get(
        "PAYLOAD_TEXT", "Hola, me gustaria recibir mas informacion sobre su producto."
    )
    target = os.environ.get("TARGET_LANGUAGE", "EN")
    result = translate_message_payload(sample_text, target_language=target)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
