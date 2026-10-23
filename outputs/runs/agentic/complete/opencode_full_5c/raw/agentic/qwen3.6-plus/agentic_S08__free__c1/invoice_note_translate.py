import os

from google.cloud import translate_v2 as translate

from document_models import TranslationResult


GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
DEFAULT_TARGET_LANGUAGE = os.getenv("DEFAULT_TARGET_LANGUAGE", "en")


def translate_invoice_note(
    text: str,
    target_language: str = DEFAULT_TARGET_LANGUAGE,
    source_language: str = "auto",
) -> TranslationResult:
    if not text or not text.strip():
        return TranslationResult(
            source_text=text or "",
            translated_text="",
            source_language=source_language,
            target_language=target_language,
            confidence=1.0,
        )

    client = translate.Client()

    translate_kwargs = {
        "q": text,
        "target_language": target_language,
        "format_": "text",
    }
    if source_language and source_language != "auto":
        translate_kwargs["source_language"] = source_language

    result = client.translate(**translate_kwargs)

    translated_text = result.get("translatedText", "")
    detected_source = result.get("detectedSourceLanguage", source_language)
    confidence = 1.0

    return TranslationResult(
        source_text=text,
        translated_text=translated_text,
        source_language=detected_source,
        target_language=target_language,
        confidence=confidence,
    )


def translate_multiple_notes(
    texts: list,
    target_language: str = DEFAULT_TARGET_LANGUAGE,
) -> list:
    if not texts:
        return []

    client = translate.Client()

    translations = []
    for text in texts:
        if not text or not text.strip():
            translations.append(
                TranslationResult(
                    source_text=text or "",
                    translated_text="",
                    source_language="auto",
                    target_language=target_language,
                    confidence=1.0,
                )
            )
            continue

        result = client.translate(
            q=text,
            target_language=target_language,
            format_="text",
        )
        translated_text = result.get("translatedText", "")
        detected_source = result.get("detectedSourceLanguage", "auto")

        translations.append(
            TranslationResult(
                source_text=text,
                translated_text=translated_text,
                source_language=detected_source,
                target_language=target_language,
                confidence=1.0,
            )
        )

    return translations
