import re
from typing import List, Dict
from speech_models import TranscriptionSegment


def moderate_transcript(
    segments: List[TranscriptionSegment],
) -> List[TranscriptionSegment]:
    """Remove profanity or disallowed content from transcript segments.

    For demonstration, we strip out any word containing 'bad' (case-insensitive).
    In production, replace this logic with a real moderation service.
    """
    moderated_segments = []
    profanity_pattern = re.compile(r"\b\\w*bad\\w*\b", re.IGNORECASE)
    for seg in segments:
        clean_text = profanity_pattern.sub(
            "█", seg["text"]
        )  # replace with mask character
        moderated_segments.append({**seg, "text": clean_text})
    return moderated_segments


# Example usage (commented out):
# if __name__ == "__main__":
#     segs = [{"text": "This is a bad example"}]
#     print(moderate_transcript(segs))
