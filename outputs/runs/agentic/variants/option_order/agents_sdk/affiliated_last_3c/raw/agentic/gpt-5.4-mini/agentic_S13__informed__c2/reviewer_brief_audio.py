from __future__ import annotations

import os

from elevenlabs.client import ElevenLabs

VOICE_ID = os.environ.get("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")


def reviewer_brief_audio(text: str) -> bytes:
    client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])
    audio = client.generate(text=text, voice=VOICE_ID, model="eleven_multilingual_v2")
    return b"".join(audio)
