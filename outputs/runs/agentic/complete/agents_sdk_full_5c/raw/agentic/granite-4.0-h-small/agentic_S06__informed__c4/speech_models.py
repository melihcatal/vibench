# speech_models.py
# Local utilities for request/response normalization and voice selection logic.

def normalize_voice_id(provider_id: str) -> str:
    """Convert a user‑friendly voice name into the exact identifier expected by the provider."""
    mapping = {
        "en-US-AlloyV2": "en-us-alloy-v2",
        "en-GB-LiamV2": "en-gb-liam-v2",
        "zh-CN-XiaoyanV2": "zh-cn-xiaoyan-v2"
    }
    return mapping.get(provider_id, provider_id)


def build_plain_request(text: str, voice_id: str | None = None) -> dict:
    """Create a request payload for plain‑text synthesis."""
    req = {
        "text": text,
        "format": "audio-8khz-16bit-mono"
    }
    if voice_id:
        req["voice"] = voice_id
    return req


def build_ssml_request(ssml: str, voice_id: str | None = None, prosody: dict | None = None) -> dict:
    """Create a request payload for SSML synthesis. Add optional prosody dict if needed."""
    req = {
        "text": ssml,
        "format": "audio-8khz-16bit-mono"
    }
    if voice_id:
        req["voice"] = voice_id
    if prosody:
        req["prosody"] = prosody
    return req

# Helper to parse provider response into a simple dict with audio_bytes
# Adjust to the exact field names returned by the provider.

def parse_response(raw: dict) -> dict:
    """Extract audio bytes and optionally metadata from the TTS response."""
    return {
        "audio_bytes": raw.get("audio_bytes", b"")
    }
