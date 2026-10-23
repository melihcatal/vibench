# [HELPER] speech_models.py
"""Local helpers for normalizing request/response models for Streaming Speech-to-Text."""

from google.cloud.speech_v1p1beta1 import types
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Request helpers
# ---------------------------------------------------------------------------


def build_streaming_request(
    audio_chunk: bytes,
    config: types.StreamingRecognitionConfig,
) -> types.StreamingRecognizeRequest:
    """Wrap an audio chunk in a StreamingRecognizeRequest."""
    return types.StreamingRecognizeRequest(audio_content=audio_chunk)


# ---------------------------------------------------------------------------
# Response / result normalization helpers
# ---------------------------------------------------------------------------


def extract_alternatives(response: Any) -> List[Dict[str, Any]]:
    """Extract alternatives from a streaming response dict."""
    try:
        return [
            {
                "transcript": alt.transcript,
                "is_final": alt.is_final,
                "confidence": alt.confidence,
            }
            for alt in response.results.alternatives
        ]
    except AttributeError:
        # When response is a simple dict rather than a protobuf object
        return [
            {
                "transcript": r.get("alternatives", [{}])[0].get("transcript", ""),
                "is_final": r.get("is_final", False),
                "confidence": r.get("confidence", None),
            }
            for r in response.get("results", [])
        ]


# ---------------------------------------------------------------------------
# Example usage (demo only)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    sample_response = {
        "results": [
            {
                "alternatives": [
                    {"transcript": "test", "is_final": True, "confidence": 0.98}
                ],
            }
        ]
    }
    print("Extracted:", extract_alternatives(sample_response))
