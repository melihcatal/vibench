import json
from typing import Dict
from deepgram import Deepgram, TranscriptResult, TranscriptWord

# ----------------------------
# Helpers for result handling
# ----------------------------


def normalize_transcript(result: TranscriptResult) -> Dict[str, str]:
    """Flatten a Deepgram result to a plain transcript string."""
    words = result.get("words", [])
    transcript = " ".join(word["word"] for word in words)
    return {
        "transcript": transcript.strip(),
        "confidence": result.get("confidence", 0.0),
    }


# Example utility to inspect word-level timing (optional)
# Not required for the core task but useful for downstream services


def extract_word_timings(result: TranscriptResult) -> Dict[int, Dict]:
    """Return a dictionary mapping start offset (seconds) to word info."""
    timings = {}
    for w in result.get("words", []):
        timings[w["start"]] = {
            "word": w["word"],
            "confidence": w.get("confidence", 0.0),
            "end": w.get("end"),
        }
    return timings


# End of helper module
