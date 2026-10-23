from google.cloud import translate_v2 as translate
from typing import List


def translate_script(
    text: str, target_language: str, source_language: str = None
) -> str:
    """
    Translates narration scripts before synthesis using Google Cloud Translation API.
    """
    client = translate.Client()

    result = client.translate(
        text, target_language=target_language, source_language=source_language
    )

    return result["translatedText"]


def batch_translate_scripts(
    texts: List[str], target_language: str, source_language: str = None
) -> List[str]:
    """
    Translates a batch of narration scripts before synthesis.
    """
    client = translate.Client()

    results = client.translate(
        texts, target_language=target_language, source_language=source_language
    )

    return [result["translatedText"] for result in results]
