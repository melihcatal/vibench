from typing import List, Dict, Any

from speech_client import SpeechClient
from speech_models import TranscriptSegment

def translate_transcript(segments: List[TranscriptSegment], target_language_code: str, config: dict = None) -> List[Dict[str, Any]]:
    config = config or {}
    region = config.get("region")
    if not region:
        raise ValueError("AWS region must be provided in config.")

    speech_client = SpeechClient(region_name=region)
    translate_client = speech_client.get_translate_client()

    translated_segments = []
    for segment in segments:
        # AWS Translate supports source language auto-detection or explicit definition.
        # For simplicity, we assume the source language is known or handled by Translate service itself.
        response = translate_client.translate_text(
            Text=segment.content,
            SourceLanguageCode="auto", # Or pass a specific source language code if known
            TargetLanguageCode=target_language_code
        )
        translated_segments.append({
            "original_segment": segment.content,
            "translated_text": response["TranslatedText"],
            "start_time": segment.start_time,
            "end_time": segment.end_time,
            "speaker_label": segment.speaker_label
        })
    return translated_segments
