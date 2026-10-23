from google.cloud import translate_v2 as translate


def batch_translate(texts, target_language="en", source_language=None):
    """
    Translate a list of strings while preserving order using Google Cloud Translation.

    Args:
        texts: List of text strings to translate
        target_language: Target language code (default: 'en')
        source_language: Source language code (optional, auto-detected if None)

    Returns:
        List of translated text strings in the same order as input
    """
    client = translate.Client()

    if source_language:
        results = client.translate(
            texts, target_language=target_language, source_language=source_language
        )
    else:
        results = client.translate(texts, target_language=target_language)

    return [result["translatedText"] for result in results]
