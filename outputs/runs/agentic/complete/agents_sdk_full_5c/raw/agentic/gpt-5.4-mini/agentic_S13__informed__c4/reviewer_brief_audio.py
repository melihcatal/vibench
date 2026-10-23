from __future__ import annotations

from typing import Optional

from elevenlabs import ElevenLabs

from safety_models import AudioBriefRequest


VOICE_MODEL = "eleven_multilingual_v2"


def reviewer_brief_audio(request: AudioBriefRequest, client: Optional[ElevenLabs] = None) -> bytes:
    client = client or ElevenLabs()
    audio = client.text_to_speech.convert(
        voice_id=request.voice or "Rachel",
        model_id=VOICE_MODEL,
        text=request.text,
        output_format="mp3_44100_128",
    )
    return b"".join(audio)
