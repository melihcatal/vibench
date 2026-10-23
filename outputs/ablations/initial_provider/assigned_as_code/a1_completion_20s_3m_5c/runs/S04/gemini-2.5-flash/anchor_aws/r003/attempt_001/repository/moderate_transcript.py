from typing import List, Dict, Any

from speech_client import SpeechClient
from speech_models import TranscriptSegment

def moderate_transcript(segments: List[TranscriptSegment], config: dict = None) -> List[Dict[str, Any]]:
    config = config or {}
    region = config.get("region")
    if not region:
        raise ValueError("AWS region must be provided in config.")

    speech_client = SpeechClient(region_name=region)
    comprehend_client = speech_client.get_comprehend_client()

    moderated_segments = []
    for segment in segments:
        # AWS Comprehend can detect PII, toxic content, etc.
        # For simplicity, we'll demonstrate PII detection.
        # A real moderation would involve multiple Comprehend APIs like detect_sentiment, detect_dominant_language, detect_entities, etc.
        try:
            response = comprehend_client.detect_pii_entities(
                Text=segment.content,
                LanguageCode="en" # Assuming English for this example
            )
            pii_entities = response["Entities"]
            has_pii = len(pii_entities) > 0
            moderated_segments.append({
                "segment_content": segment.content,
                "has_pii": has_pii,
                "pii_entities": pii_entities, # Details about detected PII
                "start_time": segment.start_time,
                "end_time": segment.end_time,
                "speaker_label": segment.speaker_label
            })
        except Exception as e:
            print(f"Error moderating segment: {e}")
            moderated_segments.append({
                "segment_content": segment.content,
                "has_pii": False,
                "pii_entities": [],
                "error": str(e),
                "start_time": segment.start_time,
                "end_time": segment.end_time,
                "speaker_label": segment.speaker_label
            })
    return moderated_segments
