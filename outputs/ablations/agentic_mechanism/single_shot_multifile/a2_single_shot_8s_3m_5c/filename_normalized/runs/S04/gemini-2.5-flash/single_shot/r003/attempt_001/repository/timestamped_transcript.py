from typing import List, Dict, Any, Optional
from speech_models import TranscriptResult

def get_word_timestamps(transcript_result: TranscriptResult) -> List[Dict[str, Any]]:
    """
    Extracts word-level timestamps and confidence from an AWS Transcribe result.
    """
    word_timestamps = []
    for item in transcript_result.items:
        if item["type"] == "pronunciation" and "start_time" in item and "end_time" in item:
            word_timestamps.append({
                "word": item["alternatives"][0]["content"],
                "start_time": float(item["start_time"]),
                "end_time": float(item["end_time"]),
                "confidence": float(item["alternatives"][0]["confidence"])
            })
    return word_timestamps

def get_segment_timestamps(transcript_result: TranscriptResult) -> List[Dict[str, Any]]:
    """
    Extracts segment-level timestamps from an AWS Transcribe result if available.
    If explicit segments are not present, it attempts to infer them from word timestamps.
    """
    if transcript_result.segments:
        # Directly use segments if provided by AWS Transcribe (e.g., from subtitle output)
        return [{
            "start_time": float(s["start_time"]),
            "end_time": float(s["end_time"]),
            "text": s["transcript"]
        } for s in transcript_result.segments if "start_time" in s and "end_time" in s and "transcript" in s]
    else:
        # Infer segments from word timestamps by grouping words into sentences/phrases.
        # This is a heuristic and might not perfectly match human-defined segments.
        word_timestamps = get_word_timestamps(transcript_result)
        if not word_timestamps:
            return []

        segments = []
        current_segment_words = []
        
        for i, word_data in enumerate(word_timestamps):
            current_segment_words.append(word_data)
            
            # Simple heuristic: End a segment on punctuation or a pause.
            is_end_of_sentence = any(p in word_data["word"] for p in [".", "?", "!", ","])
            is_long_pause = (i < len(word_timestamps) - 1 and
                             word_timestamps[i+1]["start_time"] - word_data["end_time"] > 0.5) # 0.5 seconds pause
            
            if is_end_of_sentence or is_long_pause or i == len(word_timestamps) - 1:
                if current_segment_words:
                    start_time = current_segment_words[0]["start_time"]
                    end_time = current_segment_words[-1]["end_time"]
                    text = " ".join([w["word"] for w in current_segment_words])
                    segments.append({
                        "start_time": start_time,
                        "end_time": end_time,
                        "text": text
                    })
                    current_segment_words = []
        return segments
