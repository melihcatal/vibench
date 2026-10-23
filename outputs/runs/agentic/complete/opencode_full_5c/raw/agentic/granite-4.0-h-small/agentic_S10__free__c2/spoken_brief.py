# spoken_brief.py
# [LATER-STEP]
"""Generates a spoken brief (audio) from model output using a hosted TTS service.

Demonstrates integration with a concrete Text‑to‑Speech API (e.g., Google
Cloud Text‑to‑Speech). The function returns a binary blob (e.g., mp3) that
can be saved and played.

Replace placeholder credentials with real values for actual synthesis.
"""

import os
import io
import requests
from typing import bytes

# Google Cloud TTS placeholder credentials (ENV variables)
GCLOUD_PROJECT = os.getenv("GCLOUD_PROJECT", "demo-project")
GCLOUD_TTS_KEY = os.getenv("GCLOUD_TTS_KEY", "demo-key")


def generate_spoken_brief(text: str, voice: str = "en-US-Wavenet-D") -> bytes:
    """
    Sends plain‑text to a Text‑to‑Speech endpoint and returns the audio file.

    Args:
        text (str): Prompt or generated output to be spoken.
        voice (str): Voice identifier supported by the TTS service.
    Returns:
        bytes: Binary audio data (MP3/OGG).
    """
    url = f"https://texttospeech.googleapis.com/v1/text:synthesize"
    payload = {
        "input": {"text": text},
        "voice": {"languageCode": "en-US", "name": voice},
        "audioConfig": {"audioEncoding": "MP3"},
    }
    headers = {
        "Authorization": f"Bearer {GCLOUD_TTS_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return io.BytesIO(response.json()["audioContent"])


# Example (commented to avoid auto‑execution)
# if __name__ == '__main__':
#     audio_bytes = generate_spoken_brief('Welcome to the AI brief.')
#     with open('brief.mp3', 'wb') as f:
#         f.write(audio_bytes.read())
