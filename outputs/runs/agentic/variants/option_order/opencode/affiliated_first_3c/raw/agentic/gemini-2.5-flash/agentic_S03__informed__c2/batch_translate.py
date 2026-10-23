from google.cloud import translate_v2 as translate
import os


def batch_translate_texts(
    texts: list[str], target_language: str, source_language: str = None
) -> list[str]:
    client = translate.Client()
    translations = client.translate(
        texts, target_language=target_language, source_language=source_language
    )
    return [t["translatedText"] for t in translations]
