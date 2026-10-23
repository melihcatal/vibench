from typing import TypedDict


VoiceConfig = TypedDict(
    "VoiceConfig",
    {
        "id": str,  # e.g., "cosy_1"
        "language": str,  # ISO language code like "en-US"
        "gender": str,  # "Male" / "Female" / "Neutral"
        "name": str,  # Display name
    },
)

SynthesisRequest = TypedDict(
    "SynthesisRequest",
    {
        "text": str,  # Plain text or SSML
        "format": str,  # "wav" or other audio format
        "voice": str,  # Voice ID
        "params": dict,  # Optional params (e.g., sampling_rate)
    },
)

SynthesisResponse = TypedDict(
    "SynthesisResponse",
    {
        "audio": bytes,  # Binary audio data
        "duration_ms": int,  # Optional duration
    },
)

SSMLSynthResponse = TypedDict(
    "SSMLSynthResponse",
    {
        "audio": bytes,
        "duration_ms": int,
        "ssml_input": str,  # Echo of the SSML used
    },
)
