from typing import List
from google.cloud import translate_v2 as translate
from speech_models import SpeakerLabel


def translate_transcript(segments: List[SpeakerLabel], target_language: str = "es") -> List[SpeakerLabel]:
    """
    Translate transcript segments using Google Cloud Translation.
    Returns a new list of SpeakerLabel objects with translated text.
    """
    client = translate.Client()
    translated_segments = []
    
    for segment in segments:
        result = client.translate(segment.text, target_language=target_language)
        translated_segments.append(
            SpeakerLabel(
                speaker=segment.speaker,
                text=result["translatedText"],
                start=segment.start,
                end=segment.end
            )
        )
    
    return translated_segments