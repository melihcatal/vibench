import os
from typing import Iterable, List

from google.cloud import translate_v2 as translate


def translate_live_captions(captions: Iterable[str], target_language: str) -> List[str]:
    client = translate.Client()
    results = []
    for caption in captions:
        translated = client.translate(caption, target_language=target_language, source_language=os.getenv("GOOGLE_TRANSLATE_SOURCE_LANGUAGE"))
        results.append(translated.get("translatedText", ""))
    return results
