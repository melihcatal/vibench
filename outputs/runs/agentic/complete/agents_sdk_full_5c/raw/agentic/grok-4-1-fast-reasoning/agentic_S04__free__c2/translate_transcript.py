from google.cloud import translate_v2 as translate
from typing import List

def translate_transcript(transcript_segments: List[str], target_language: str = "es") -> List[str]:
    """
    Translate completed transcript segments using Google Cloud Translate.
    """
    client = translate.Client()
    results = client.translate(transcript_segments, target_language=target_language)
    return [result["translatedText"] for result in results]