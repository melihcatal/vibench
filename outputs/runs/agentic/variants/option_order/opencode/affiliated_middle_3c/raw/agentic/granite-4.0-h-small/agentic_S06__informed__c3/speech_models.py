# HELPER: speech_models.py
# Local request, response, and normalization utilities for Watson TTS

from typing import Dict, Any
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.http import HTTPRequest, HTTPMethod


def build_synthesize_params(
    text: str,
    ssml: str = None,
    voice: str = "en-US_MichaelV3Voice",
    accept: str = "audio/flac",
) -> Dict[str, Any]:
    """Normalize and build parameters for synthesize_speech calls.

    Accepts either plain text or SSML; the other must be None.
    """
    if (text and ssml) or (text is None and ssml is None):
        raise ValueError("Provide exactly one of text or ssml.")
    params = {"accept": accept, "voice": voice}
    if text:
        params["text"] = text
    if ssml:
        params["ssml"] = ssml
    return params


def parse_audio_response(response: TextToSpeechV1) -> bytes:
    """Extract raw audio bytes from Watson TTS SDK response.

    The SDK returns a streaming body; this helper reads it entirely.
    """
    return response.get_result().read()


# Example demonstration
if __name__ == "__main__":
    client = (
        get_client()
    )  # from speech_client.py (ensure it's imported or defined here)
    params = build_synthesize_params(text="Hello, world!")
    response = client.synthesize_speech(**params)
    audio = parse_audio_response(response)
    print("First 10 bytes of audio:", audio[:10])
