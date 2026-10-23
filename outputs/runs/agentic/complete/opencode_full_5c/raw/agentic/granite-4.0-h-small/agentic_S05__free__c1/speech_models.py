from typing import Dict, Any

from google.cloud.speech_v1p1beta1 import (
    SpeechRecognitionResult,
    StreamingRecognizeResponse,
    SpeechRecognitionAlternative,
)

# ----------------------------
# Response parsing utilities
# ----------------------------


def extract_alternatives(response: StreamingRecognizeResponse) -> list[Dict[str, Any]]:
    """Return a list of alternative dicts from the response."""
    alternatives = []
    for result in response.results:
        if result.alternatives:
            alt = result.alternatives[0]
            alternatives.append(
                {
                    "transcript": alt.transcript,
                    "confidence": alt.confidence,
                    "is_final": result.is_final,
                }
            )
    return alternatives


# ----------------------------
# Normalization helpers
# ----------------------------


def normalize_transcript(text: str) -> str:
    """
    Simple normalization: trim whitespace, replace multiple spaces with one,
    and remove control characters.
    """
    import re

    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[\\x00-\\x1F]", "", text)
    return text


# Example: batch normalization of a list of alternatives
if __name__ == "__main__":
    # Simulated response payload (copy of extract_alternatives output)
    responses = [
        {
            "transcript": " Hello   world ",
            "confidence": 0.92,
            "is_final": False,
        },
        {
            "transcript": " This is a test . ",
            "confidence": 0.96,
            "is_final": True,
        },
    ]
    normalized = [normalize_transcript(item["transcript"]) for item in responses]
    print("Normalized transcripts:")
    print(normalized)
