from typing import Iterable, List

from google.cloud import translate_v2 as translate

from speech_models import normalize_transcript


def translate_live_captions(chunks: Iterable[str], target_language: str) -> List[str]:
    client = translate.Client()
    return [normalize_transcript(client.translate(chunk, target_language=target_language)["translatedText"]) for chunk in chunks if chunk]
