# [SAME-SCENARIO] partial_results.py
# Handles partial and final streaming recognition events from Deepgram

import json

# Dummy normalization helper to illustrate handling of partial results
NORMALIZE_PUNCTUATION = True

# Mapping of Deepgram fields to normalized transcript format
MODEL_TO_TARGET = {"nordic": "en-US"}

# Helper to extract interim text


def get_interim(data):
    """
    Returns the interim transcript string from a streaming result object.
    Handles both partial 'interim' events and final 'result' events.
    """
    try:
        alternatives = data["result"].get("alternatives", [])
        if alternatives:
            transcript = alternatives[0].get("transcript", "")
            if not NORMALIZE_PUNCTUATION:
                return transcript
            # Simple post‑processing: capitalize sentence‑start, add periods, etc.
            return transcript.capitalize()
    except KeyError:
        return ""
    return ""


# Example usage (for illustration only)
if __name__ == "__main__":
    # Simulated streaming response from Deepgram
    sample = {
        "result": {
            "alternatives": [{"transcript": "hello world this is a partial transcript"}]
        }
    }
    print("Interim (raw):", get_interim(sample))
    print("Interim (normalized):", get_interim(sample) if NORMALIZE_PUNCTUATION else "")
