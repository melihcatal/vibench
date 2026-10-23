# [HELPER] speech_models.py
# Define local request, response, and normalization helpers for Streaming Speech-to-Text
from typing import Dict, Any
from datetime import datetime

# Common response shape for both providers
ResponseShape = Dict[str, Any]

STATUS_PENDING = "pending"
STATUS_FINAL = "final"


def normalize_response(provider: str, raw: Any) -> ResponseShape:
    """Convert provider-specific streaming result into a unified dict."""
    if provider == "google":
        # Google Speech client result
        result = raw.results[0] if raw.results else None
        if not result:
            return None
        alternative = result.alternatives[0]
        return {
            "provider": provider,
            "transcript": alternative.transcript,
            "is_final": result.is_final,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    elif provider == "openai":
        # OpenAI Whisper streaming chunk (JSON line)
        # Assume raw is a dict with 'text' and optional 'done' flag
        return {
            "provider": provider,
            "transcript": raw.get("text", ""),
            "is_final": raw.get("done", False),
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    else:
        raise ValueError(f"Unsupported provider: {provider}")


# Example usage (uncomment to test)
# def test_google():
#     from google.cloud.speech_v1p1beta1 import StreamingRecognizeResponse
#     sample = StreamingRecognizeResponse(
#         result=StreamingRecognizeResponse.Result(alternatives=[
#             StreamingRecognizeResponse.Alternative(transcript="Hello world", is_final=False)
#         ], is_final_result=True)
#     )
#     print(normalize_response("google", sample))

# def test_openai():
#     sample = {"text": "Bonjour", "done": False}
#     print(normalize_response("openai", sample))
