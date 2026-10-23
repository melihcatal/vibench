from __future__ import annotations

import base64

from openai import OpenAI

from safety_client import safety_model_name
from safety_models import AudioResult


AUDIO_PROMPT = """Generate a concise spoken brief for a moderation reviewer.\n"""


def reviewer_brief_audio(text: str) -> AudioResult:
    client = OpenAI()
    response = client.audio.speech.create(  # openai SDK
        model=safety_model_name("audio"),
        voice="alloy",
        input=f"{AUDIO_PROMPT}\n{text}",
        format="mp3",
    )
    audio_bytes = response.read()
    return AudioResult(audio_base64=base64.b64encode(audio_bytes).decode("ascii"), format="mp3")
