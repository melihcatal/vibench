import json
from typing import Dict, Any

# Provider-specific response normalization helpers


def normalize_deepgram_response(response: Dict[str, Any]) -> str:
    """Convert Deepgram streaming response dict to plain transcript text."""
    # Deepgram streaming returns a list of results under "results"
    transcript_parts = []
    for result in response.get("results", []):
        alternative = result.get("alternatives", [{}])[0]
        transcripts = alternative.get("transcript", "")
        # Append transcript, respecting partial flag if needed
        transcript_parts.append(transcripts)
    return " ".join(transcript_parts)


def normalize_google_response(response: Dict[str, Any]) -> str:
    """Convert Google Cloud Speech Streaming response dict to plain transcript text."""
    transcript_parts = []
    for result in response.get("results", []):
        alternative = result.get("alternatives", [{}])[0]
        transcript_parts.append(alternative.get("transcript", ""))
    return " ".join(transcript_parts)


def normalize_amazon_response(response: Dict[str, Any]) -> str:
    """Convert Amazon Transcribe Streaming response dict to plain transcript text."""
    transcript_parts = []
    for result in response.get("results", []):
        for alt in result.get("alternatives", []):
            transcript_parts.append(alt.get("transcript", ""))
    return " ".join(transcript_parts)


# Example usage (not executed)
# if __name__ == "__main__":
#     sample_deep = {"results":[{"alternatives":[{"transcript":"Hello "}]}]}
#     print(normalize_deepgram_response(sample_deep))
