import os
from google.cloud import translate
from typing import List, Dict, Any
from speech_models import TranscriptSegment

def translate_transcript(segments: List[TranscriptSegment], target_language_code: str, project_id: str) -> List[TranscriptSegment]:
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    translated_segments = []
    for segment in segments:
        response = client.translate_text(
            parent=parent,
            contents=[segment.text],
            target_language_code=target_language_code,
            source_language_code="en" # Assuming source language is English from transcription
        )
        translated_text = response.translations[0].translated_text
        translated_segments.append(TranscriptSegment(
            start_time=segment.start_time,
            end_time=segment.end_time,
            text=translated_text,
            speaker=segment.speaker,
            words=None # Word level translation is not done here
        ))
    return translated_segments
