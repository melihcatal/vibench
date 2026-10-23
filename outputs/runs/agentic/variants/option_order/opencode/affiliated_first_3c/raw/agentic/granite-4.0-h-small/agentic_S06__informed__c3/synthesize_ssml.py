# [SAME-SCENARIO] synthesize_ssml.py
# Synthesizes SSML with voice and prosody controls using ElevenLabs Text-to-Speech

import os
import requests
from typing import bytes

# ---------- Configuration ----------
# Provider: ElevenLabs (identified by SDK import and API key)
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
BASE_URL = "https://api.elevenlabs.io/v1/text-to-speech"
# -----------------------------------


def synthesize_ssml(ssml: str, voice_name: str = "lyra") -> bytes:
    """Synthesize SSML to raw audio bytes.

    Args:
        ssml (str): SSML string containing speech markup.
        voice_name (str): ElevenLabs voice identifier (default: 'lyra').

    Returns:
        bytes: The synthesized PCM audio data.
    """
    if not ELEVENLABS_API_KEY:
        raise RuntimeError("ELEVENLABS_API_KEY environment variable not set")

    payload = {
        "text": ssml,
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
    return response.content


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     ssml = "<speak>Hello, <break time='500ms'/> world!</speak>"
#     audio = synthesize_ssml(ssml)
#     with open("output.raw", "wb") as f:
#         f.write(audio)
