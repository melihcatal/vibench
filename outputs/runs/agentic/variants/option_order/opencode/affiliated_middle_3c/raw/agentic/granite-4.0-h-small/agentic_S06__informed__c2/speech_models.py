from typing import Dict, Literal

# Normalized request/response models for all providers (Azure used as example)

SynthesisRequest = Dict[str, Any]
SynthesisResponse = Dict[str, Any]


class SynthesisStatus(Literal["SUCCEEDED", "FAILED", "QUEUED", "CANCELLED"]): ...


def normalize_synth_response(
    provider_name: str, raw: Dict[str, Any]
) -> SynthesisResponse:
    """Convert provider‑specific responses into a common shape:
    {
        'status': SynthesisStatus,
        'audio_bytes': bytes,
        'metadata': Dict[str, Any]
    }
    """
    if provider_name.lower() == "azure":
        # Azure response example: result.audio_data holds bytes; result.reason holds status
        return {
            "status": SynthesisStatus.SUCCEEDED
            if raw.get("reason") == "Success"
            else SynthesisStatus.FAILED,
            "audio_bytes": raw.get("audio_data", b""),
            "metadata": {
                "request_id": raw.get("request_id"),
                "voice_name": raw.get("voice_name"),
            },
        }
    # Add other providers here as needed
    raise ValueError(f"Unsupported provider for normalization: {provider_name}")


# Example usage (for testing only)
if __name__ == "__main__":
    dummy = {
        "reason": "Success",
        "audio_data": b"\x00\x01\x02",
        "request_id": "12345",
        "voice_name": "en-US-JennyNeural",
    }
    print(normalize_synth_response("azure", dummy))
