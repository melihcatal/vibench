from google.cloud import translate_v2 as translate
from speech_models import TranscriptSegment
from typing import List

def translate_transcript(segments: List[TranscriptSegment], target_language: str = "es") -> List[TranscriptSegment]:
    """Translate completed transcript segments using Google Cloud Translation API."""
    client = translate.Client()
    
    translated_segments = []
    for segment in segments:
        result = client.translate(
            segment.text,
            target_language=target_language,
            model="nmt"  # Google Cloud-specific model identifier
        )
        translated_segments.append(
            TranscriptSegment(
                text=result["translatedText"],
                start_time=segment.start_time,
                end_time=segment.end_time,
            )
        )
    
    return translated_segments