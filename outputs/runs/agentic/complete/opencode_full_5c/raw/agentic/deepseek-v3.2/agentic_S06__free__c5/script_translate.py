from google.cloud import translate_v2 as translate


def translate_narration_script(text, target_language="en", source_language=None):
    """Translate narration scripts before synthesis using Google Cloud Translation."""
    translate_client = translate.Client()

    if source_language:
        result = translate_client.translate(
            text, target_language=target_language, source_language=source_language
        )
    else:
        result = translate_client.translate(text, target_language=target_language)

    return {
        "translated_text": result["translatedText"],
        "source_language": result.get("detectedSourceLanguage", source_language),
        "target_language": target_language,
    }


def translate_batch_narration_scripts(texts, target_language="en"):
    """Translate multiple narration scripts in batch."""
    translate_client = translate.Client()

    results = translate_client.translate(texts, target_language=target_language)

    translations = []
    for result in results:
        translations.append(
            {
                "original": result["input"],
                "translated": result["translatedText"],
                "source_language": result.get("detectedSourceLanguage"),
            }
        )

    return translations
