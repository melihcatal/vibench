import os
from google.cloud import translate
from speech_models import TranscriptSegment
from typing import List

def translate_transcript_segments(segments: List[TranscriptSegment], target_language: str) -> List[TranscriptSegment]:
    client = translate.TranslationServiceClient()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable must be set.")

    parent = f"projects/{project_id}/locations/global"

    translated_segments = []
    for segment in segments:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [segment.text],
                "target_language_code": target_language,
            }
        )

        translated_text = response.translations[0].translated_text
        translated_segments.append(TranscriptSegment(
            id=segment.id,
            start=segment.start,
            end=segment.end,
            text=translated_text,
            speaker=segment.speaker
        ))
    return translated_segments
