"""
Return word or segment timestamps from a transcription result.
Provider: Deepgram (api.deepgram.com)
SDK: deepgram-sdk with nova-2 model for word-level timestamp extraction.
"""

import logging
from typing import List, Dict, Any, Optional

from speech_client import create_deepgram_client
from speech_models import (
    normalize_deepgram_response,
    format_timestamped_transcript,
    TranscriptionResponse,
    WordResult,
)

logger = logging.getLogger(__name__)

DEEPGRAM_API_HOST = "api.deepgram.com"
TIMESTAMP_MODEL = "nova-2"


def get_timestamped_transcription(
    request_id: str,
) -> TranscriptionResponse:
    """
    Retrieve a transcription with word-level timestamps from Deepgram.
    
    Uses Deepgram's api.deepgram.com nova-2 model which provides
    precise word-level start and end times in the response.
    
    Args:
        request_id: The Deepgram request ID
        
    Returns:
        TranscriptionResponse with word-level timing data
    """
    client = create_deepgram_client()
    listen_client = client.listen
    
    response = listen_client.get_request(request_id)
    response_data = response.to_dict()
    
    status = response_data.get("response", {}).get("status", "unknown")
    if status != "completed":
        raise ValueError(
            f"Transcription job {request_id} is not completed (status: {status})"
        )
    
    raw_response = response_data.get("response", {})
    normalized = normalize_deepgram_response(raw_response)
    
    return normalized


def get_word_timestamps(
    request_id: str,
) -> List[Dict[str, Any]]:
    """
    Extract word-level timestamps from a Deepgram transcription.
    
    Each word includes start time, end time, confidence, and speaker (if diarized).
    Provider: Deepgram api.deepgram.com nova-2 model.
    """
    response = get_timestamped_transcription(request_id)
    
    timestamps = []
    for word in response.words:
        timestamps.append({
            "word": word.word,
            "start": word.start,
            "end": word.end,
            "confidence": word.confidence,
            "speaker": word.speaker,
            "punctuated": word.punctuated_word or word.word,
        })
    
    return timestamps


def get_segment_timestamps(
    request_id: str,
    segment_duration: float = 30.0,
) -> List[Dict[str, Any]]:
    """
    Group words into time segments with start/end timestamps.
    
    Chunks the Deepgram transcription into segments of specified duration.
    Useful for subtitle generation or chapter markers.
    """
    response = get_timestamped_transcription(request_id)
    
    if not response.words:
        return []
    
    segments = []
    current_segment_words = []
    segment_start = response.words[0].start
    segment_end = segment_start
    
    for word in response.words:
        if word.start - segment_start >= segment_duration:
            # Finalize current segment
            segment_text = " ".join(w.punctuated_word or w.word for w in current_segment_words)
            segments.append({
                "start": segment_start,
                "end": segment_end,
                "duration": segment_end - segment_start,
                "text": segment_text,
                "word_count": len(current_segment_words),
            })
            
            # Start new segment
            current_segment_words = [word]
            segment_start = word.start
            segment_end = word.end
        else:
            current_segment_words.append(word)
            segment_end = max(segment_end, word.end)
    
    # Add final segment
    if current_segment_words:
        segment_text = " ".join(w.punctuated_word or w.word for w in current_segment_words)
        segments.append({
            "start": segment_start,
            "end": segment_end,
            "duration": segment_end - segment_start,
            "text": segment_text,
            "word_count": len(current_segment_words),
        })
    
    return segments


def format_with_timestamps(
    request_id: str,
) -> str:
    """
    Format transcription with inline timestamps.
    
    Returns human-readable transcript with [start-end] timestamps per word.
    Uses Deepgram's precise word timing from api.deepgram.com.
    """
    response = get_timestamped_transcription(request_id)
    return format_timestamped_transcript(response)


def export_srt(
    request_id: str,
    max_line_words: int = 8,
) -> str:
    """
    Export transcription as SRT subtitle format with timestamps.
    
    Uses Deepgram word-level timing to create standard SRT output.
    """
    response = get_timestamped_transcription(request_id)
    
    if not response.words:
        return ""
    
    def format_srt_time(seconds: float) -> str:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        millis = int((secs - int(secs)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{int(secs):02d},{millis:03d}"
    
    srt_lines = []
    subtitle_index = 1
    current_words = []
    
    for word in response.words:
        current_words.append(word)
        
        if len(current_words) >= max_line_words or word.word.endswith((".", "!", "?")):
            start_time = format_srt_time(current_words[0].start)
            end_time = format_srt_time(current_words[-1].end)
            text = " ".join(w.punctuated_word or w.word for w in current_words)
            
            srt_lines.append(f"{subtitle_index}")
            srt_lines.append(f"{start_time} --> {end_time}")
            srt_lines.append(text)
            srt_lines.append("")
            
            subtitle_index += 1
            current_words = []
    
    # Handle remaining words
    if current_words:
        start_time = format_srt_time(current_words[0].start)
        end_time = format_srt_time(current_words[-1].end)
        text = " ".join(w.punctuated_word or w.word for w in current_words)
        
        srt_lines.append(f"{subtitle_index}")
        srt_lines.append(f"{start_time} --> {end_time}")
        srt_lines.append(text)
    
    return "\n".join(srt_lines)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        request_id = sys.argv[1]
        formatted = format_with_timestamps(request_id)
        print(formatted)
    else:
        print("Usage: python timestamped_transcript.py <request_id>")
