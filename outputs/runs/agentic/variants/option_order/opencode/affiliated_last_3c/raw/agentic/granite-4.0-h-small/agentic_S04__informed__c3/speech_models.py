from typing import Dict, List, Any

#
# Request / response data models for Batch Speech-to-Text operations
#

TranscriptionRequest = Dict[str, Any]
TranscriptionResponse = Dict[str, Any]

# Normalized result type after parsing Amazon Transcribe output
NormalizedTranscript = List[
    Dict[str, Any]
]  # [{"start": float, "duration": float, "text": str}, ...]

#
# Helper for normalizing different provider timestamps into the same shape
#


def normalize_timestamps(
    provider_response: TranscriptionResponse,
) -> NormalizedTranscript:
    """Converts raw provider response into a consistent list of timestamped segments."""
    # Placeholder implementation for Amazon Transcribe
    # Replace with actual parsing logic for other providers as needed
    segments = []
    for seg in provider_response.get("Results", []):
        for alt in seg.get("Alternatives", []):
            for word in alt.get("Items", []):
                segments.append(
                    {
                        "start": word.get("Start") or 0.0,
                        "duration": word.get("Duration") or 0.0,
                        "text": word.get("Content", ""),
                    }
                )
    return segments
