import os
import deepl
from messaging_models import TranslationResult, extract_text_from_payload


def translate_message_payload(
    message_id: str,
    payload: dict,
    target_language: str = "ES",
    source_language: str = "EN",
) -> TranslationResult:
    auth_key = os.environ.get("DEEPL_AUTH_KEY", "")
    translator = deepl.Translator(auth_key)
    text = extract_text_from_payload(payload)
    if not text:
        return TranslationResult(
            message_id=message_id,
            original_text="",
            translated_text="",
            source_language=source_language,
            target_language=target_language,
            success=False,
            error="No translatable text found in payload",
        )
    try:
        result = translator.translate_text(
            text,
            source_lang=source_language,
            target_lang=target_language,
        )
        return TranslationResult(
            message_id=message_id,
            original_text=text,
            translated_text=result.text,
            source_language=source_language,
            target_language=target_language,
            success=True,
        )
    except Exception as e:
        return TranslationResult(
            message_id=message_id,
            original_text=text,
            translated_text="",
            source_language=source_language,
            target_language=target_language,
            success=False,
            error=str(e),
        )


if __name__ == "__main__":
    result = translate_message_payload(
        message_id="evt-001",
        payload={"text": "Welcome to our platform! We are glad to have you."},
        target_language="ES",
        source_language="EN",
    )
    print(result.to_dict())
