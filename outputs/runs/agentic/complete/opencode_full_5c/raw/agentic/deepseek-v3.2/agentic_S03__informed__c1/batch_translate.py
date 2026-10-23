import os
from google.cloud import translate_v2 as translate


def batch_translate(texts, target_language="en", source_language=None):
    """Translate a list of strings while preserving order using Google Cloud Translation."""
    client = translate.Client()

    kwargs = {"target_language": target_language, "values": texts}
    if source_language:
        kwargs["source_language"] = source_language

    results = client.translate(**kwargs)

    translations = []
    for i, result in enumerate(results):
        translations.append(
            {
                "original_text": texts[i],
                "translated_text": result["translatedText"],
                "source_language": result.get(
                    "detectedSourceLanguage", source_language
                ),
                "target_language": target_language,
                "index": i,
            }
        )

    return translations
