import os
from google.cloud import translate_v2 as translate


def batch_translate(texts: list[str], source_lang: str, target_lang: str) -> list[str]:
    client = translate.Client()
    results = client.translate(
        texts, source_language=source_lang, target_language=target_lang
    )
    return [result["translatedText"] for result in results]
