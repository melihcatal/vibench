from typing import Dict, Any, List

from speech_models import normalize_transcript_result

def get_word_timestamps(transcript_content: Dict[str, Any]) -> List[Dict[str, Any]]:
    # Assuming transcript_content is the output from normalize_transcript_result
    return transcript_content.get("word_timestamps", [])

def get_segment_timestamps(transcript_content: Dict[str, Any]) -> List[Dict[str, Any]]:
    # Assuming transcript_content is the output from normalize_transcript_result
    # This will return segments from diarization if available, otherwise it's just words.
    # For segment timestamps without diarization, one might need to re-process words into sentences/phrases.
    # For this task, if diarization segments are present, we return those. Otherwise, we return word timestamps.
    diarization_segments = transcript_content.get("diarization_segments", [])
    if diarization_segments:
        return diarization_segments
    else:
        # If no diarization, we can consider each word as a segment for timestamping
        return transcript_content.get("word_timestamps", [])
