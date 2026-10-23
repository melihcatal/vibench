# [SAME-SCENARIO] synthesize_text.py
# Synthesizes plain text to an audio byte stream using ElevenLabs Text-to-Speech

import os
import requests
from typing import bytes

# ---------- Configuration ----------
# Provider: ElevenLabs (identified by SDK import and API key)
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
BASE_URL = "https://api.elevenlabs.io/v1/text-to-speech"
# -----------------------------------


def synthesize_text(text: str, voice_name: str = "lyra") -> bytes:
    """Synthesize plain text to raw audio bytes.

    Args:
        text (str): The text to convert.
        voice_name (str): ElevenLabs voice identifier (default: 'lyra').

    Returns:
        bytes: The synthesized PCM audio data.
    """
    if not ELEVENLABS_API_KEY:
        raise RuntimeError("ELEVENLABS_API_KEY environment variable not set")

    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_name": voice_name,
        "audio_format": "pcm_f32le",
    }
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
    }
    response = requests.post(BASE_URL, json=payload, headers=headers)
    response.raise_for_status()
    # audio data is returned as binary in the response body
    return response.content


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     audio = synthesize_text("Hello, world!")
#     with open("output.raw", "wb") as f:
#         f.write(audio)
