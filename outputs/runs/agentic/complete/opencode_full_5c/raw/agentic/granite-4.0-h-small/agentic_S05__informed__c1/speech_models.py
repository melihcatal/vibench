# [HELPER] speech_models.py
# Local request, response, and normalization helpers for Streaming Speech-to-Text

import json

# ----------------------------------------------------------------------
# Request helpers (model identifiers, language codes, etc.)
# ----------------------------------------------------------------------

# Deepgram model identifiers (fits model ID requirement)
DEEPGRAM_MODELS = {
    "english": "nordic",
    "spanish": "latam",
    "french": "francais",
}

# Normalization helpers
NORMALIZE_PUNCTUATION = True  # global toggle (could be per‑session)


# Mapping of raw provider fields to a normalized transcript format
def normalize_transcript(raw_result: dict) -> str:
    """Extracts and optionally post‑processes the transcript string."""
    try:
        alternatives = raw_result.get("result", {}).get("alternatives", [])
        if not alternatives:
            return ""
        transcript = alternatives[0].get("transcript", "")
        if not NORMALIZE_PUNCTUATION:
            return transcript
        # Simple normalization: capitalize sentence start
        return transcript.capitalize()
    except Exception:
        return ""


# ----------------------------------------------------------------------
# Example usage (illustrative only)
# ----------------------------------------------------------------------

if __name__ == "__main__":
    sample_deepgram = {
        "result": {"alternatives": [{"transcript": "hello world this is a test"}]}
    }
    print("Normalized transcript:", normalize_transcript(sample_deepgram))
