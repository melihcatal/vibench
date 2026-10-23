from google.cloud import translate_v2 as translate


def multilingual_query_translate(query: str, target_language: str = "en"):
    """Translates text into the target language.

    Target language defaults to English, but can be any ISO 639-1 language code.
    """
    translate_client = translate.Client()

    result = translate_client.translate(query, target_language=target_language)

    return {
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"],
    }
