# Helper utilities for request/response normalization and validation

import os
from typing import Dict, Any

# Example import for Azure Speech (uncomment if using Azure)
# from azure.cognitiveservices.speech import AudioDataStream

# Example import for Google TTS (uncomment if using Google)
# from google.cloud import texttospeech

# Example import for AWS Polly (uncomment if using AWS)
# import boto3

# ---------------------------------------------------------------------------
# Request normalization helpers
# ---------------------------------------------------------------------------


def build_speech_request(
    text: str = None,
    ssml: str = None,
    voice_name: str = None,
    prosody_pitch: float = 0.0,
    prosody_rate: float = 1.0,
) -> Dict[str, Any]:
    """Create a provider‑agnostic payload dict for TTS synthesis.

    Args:
        text (str): Plain text fallback.
        ssml (str): SSML string.
        voice_name (str): Voice identifier.
        prosody_pitch (float): Pitch multiplier.
        prosody_rate (float): Speaking rate.

    Returns:
        dict: Normalized request dictionary.
    """
    payload = {
        "text": text,
        "ssml": ssml,
        "voice_name": voice_name,
        "prosody": {
            "pitch": prosody_pitch,
            "rate": prosody_rate,
        },
    }
    # Remove keys with None values for cleaner SDK calls
    return {k: v for k, v in payload.items() if v is not None}


# ---------------------------------------------------------------------------
# Response normalization & simple validation
# ---------------------------------------------------------------------------


def normalize_audio_response(raw: bytes) -> bytes:
    """Placeholder for any post‑processing (e.g., format conversion)."""
    return raw


def validate_audio_bytes(data: bytes) -> None:
    """Simple sanity check – non‑empty byte stream."""
    if not data:
        raise ValueError("Synthesized audio is empty")


# ---------------------------------------------------------------------------
# Example provider‑specific extraction functions (select ONE provider)
# ---------------------------------------------------------------------------
# def extract_audio_from_azure(stream: AudioDataStream) -> bytes:
#     return stream.get_audio()
#
# def extract_audio_from_google(response: texttospeech.SynthesizeSpeechResponse) -> bytes:
#     return response.audio_content
#
# def extract_audio_from_polly(response: Dict) -> bytes:
#     return response['AudioStream'].read()

# ---------------------------------------------------------------------------
# Normalized wrapper that can be used by downstream modules
# ---------------------------------------------------------------------------


def synthesize_with_client(client, request_args: Dict[str, Any]) -> bytes:
    """Use provider client to generate audio bytes, perform basic validation.

    Args:
        client (TextToSpeechClient): Instantiated provider client.
        request_args (dict): Normalized request dict.

    Returns:
        bytes: Validated audio byte stream.
    """
    # Call client based on which arguments are present
    if request_args.get("ssml"):
        audio = client.synthesize_speech(
            input_ssml=request_args["ssml"],
            voice_name=request_args.get("voice_name"),
            prosody_pitch=request_args["prosody"].get("pitch"),
            prosody_rate=request_args["prosody"].get("rate"),
        )
    else:
        audio = client.synthesize_speech(
            input_text=request_args["text"], voice_name=request_args.get("voice_name")
        )
    # Validate and normalize
    validate_audio_bytes(audio)
    return normalize_audio_response(audio)
