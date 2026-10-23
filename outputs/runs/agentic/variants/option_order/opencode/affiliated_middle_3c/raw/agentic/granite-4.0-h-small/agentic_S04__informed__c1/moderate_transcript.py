import json
from speech_models import TranscriptionResult, normalize_transcript
from moderation_client import ContentModerator

TRANSLATE_WHITELIST = {"en", "es", "fr", "de", "zh", "ja"}

def moderate_transcript(transcript: TranscriptionResult, allowed_content: set = None) -> TranscriptionResult:
    """Run a safety check and optionally filter/moderate transcript segments.

    Args:
        transcript (TranscriptionResult): Normalized transcript with segments.
        allowed_content (set): Optional set of allowed language codes. If None,
                               a default whitelist is used.

    Returns:
        TranscriptionResult: Same structure, with offensive segments removed/replaced.
    """
    if allowed_content is None:
        allowed_content = TRANSLATE_WHITELIST
    moderator = ContentModerator()\n    moderated_segments = []
    for seg in transcript["segments"]:
        # 1. Language detection (stubbed)
        lang = detect_language(seg["text"])
        if lang not in allowed_content:
            # Skip or replace offensive content
            moderated_segments.append({"start": seg["start"], "end": seg["end"], "text": "[INAPPROPRIATE LANGUAGE DETECTED]"})
            continue
        # 2. Content safety check (stubbed)
        if moderator.is_offensive(seg["text"]):
            moderated_segments.append({"start": seg["start"], "end": seg["end"], "text": "[MODERATED CONTENT]"})
        else:
            moderated_segments.append(seg)
    return TranscriptionResult(status=transcript["status"], segments=moderated_segments)

# Helper placeholder for language detection

def detect_language(text: str) -> str:
    # Stub: in production, use a language detection API or library
    return "en"

# Example (uncomment to test)
# if __name__ == "__main__":
#     job = {"job_id": "job_123", "language": "en"}
#     result = poll_transcription(job["job_id"])
#     norm = normalize_transcript(result)
#     safe = moderate_transcript(norm)
#     print(json.dumps(safe, indent=2))