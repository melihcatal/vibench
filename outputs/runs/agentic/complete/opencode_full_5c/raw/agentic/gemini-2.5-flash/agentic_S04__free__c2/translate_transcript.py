from google.cloud import translate_v2 as translate
from typing import List


def translate_transcript_segments(
    segments: List[str], target_language: str
) -> List[str]:
    client = translate.Client()
    translations = client.translate(segments, target_language=target_language)
    return [translation["translatedText"] for translation in translations]
