import json
from typing import List, Dict
from speech_models import TranscriptionSegment


def archive_summary(segments: List[TranscriptionSegment]) -> Dict[str, int]:
    """Produce a concise summary of the transcription result.

    Returns a dictionary with total word count and approximate duration (seconds).
    """
    word_count = sum(1 for seg in segments if seg["text"].strip())
    total_duration = max((seg["end"] for seg in segments), default=0) - min(
        (seg["start"] for seg in segments), default=0
    )
    summary = {"total_words": word_count, "duration_seconds": round(total_duration, 2)}
    # Persisting to an archive (e.g., S3) would happen here.
    return summary


# Example invocation (commented out):
# if __name__ == "__main__":
#     segments = [{"text":"Hello"},{"text":"world"}]
#     print(json.dumps(archive_summary(segments), indent=2))
