# [LATER-STEP] spoken_brief.py

import os
import requests

class ElevenLabsTTS:
    """Wrapper around ElevenLabs Text-to-Speech API to generate a spoken brief."""
    BASE_URL = "https://api.elevenlabs.io/v1/text-to-speech"
    API_KEY = os.getenv("ELEVENLABS_API_KEY")
    if not API_KEY:
        raise RuntimeError("Set ELEVENLABS_API_KEY environment variable")

    @staticmethod
    def generate_speech(text: str, voice: str = "emery") -> bytes:
        payload = {
            "text": text,
            "voice_id": voice,
            "model_id": "eleven_monolingual_v1"
        }
        headers = {
            "xi-api-key": ElevenLabsTTS.API_KEY,
            "Content-Type": "application/json"
        }
        resp = requests.post(ElevenLabsTTS.BASE_URL, json=payload, headers=headers)
        resp.raise_for_status()
        # The API returns audio binary data
        return resp.content
