# speech_models.py
# [HELPER]
# Define local request, response, and normalization helpers for Streaming Speech-to-Text

from typing import Dict, Any, List

# Type alias for Deepgram streaming recognition response
RecognitionResult = Dict[str, Any]


def normalize_transcript(result: RecognitionResult) -> str:
    """Extract and clean the transcript string from a recognition result."""
    try:
        transcript = result["results"][0]["alternatives"][0]["transcript"]
        # Simple post-processing: strip whitespace and collapse multiple spaces
        clean = " ".join(transcript.split())
        return clean
    except (KeyError, IndexError, TypeError):
        return ""


def extract_alternatives(result: RecognitionResult) -> List[str]:
    """Return a list of all alternative transcripts found in the result."""
    alternatives = []
    for res in result.get("results", []):
        alts = [alt["transcript"] for alt in res.get("alternatives", [])]
        alternatives.extend(alts)
    return alternatives


def is_final(result: RecognitionResult) -> bool:
    """Check whether a streaming result indicates the final transcription (no interim flag)."""
    return not any(r.get("is_interim", False) for r in result.get("results", []))


# Example usage for testing
if __name__ == "__main__":
    # Dummy result mimicking Deepgram format
    dummy = {"results": [{"alternatives": [{"transcript": "Hello world"}]}]}
    print("Normalized:", normalize_transcript(dummy))
    print("Final?", is_final(dummy))
