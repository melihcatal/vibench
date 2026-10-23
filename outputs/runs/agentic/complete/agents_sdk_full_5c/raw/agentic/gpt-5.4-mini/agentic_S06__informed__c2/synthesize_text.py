from __future__ import annotations

from io import BytesIO
from typing import Optional

from speech_client import create_polly_client, load_config
from speech_models import SpeechRequest, SpeechResponse, normalize_text


def synthesize_text(text: str, voice_name: Optional[str] = None, locale: Optional[str] = None) -> bytes:
    request = SpeechRequest(text=normalize_text(text), voice_name=voice_name, locale=locale, ssml=False)
    client = create_polly_client(load_config())
    response = client.synthesize_speech(
        Text=request.text,
        VoiceId=request.voice_name or "Joanna",
        OutputFormat="mp3",
    )
    audio_stream = response["AudioStream"].read()
    SpeechResponse(audio=audio_stream, provider="amazon-polly", metadata={"request": request.__dict__})
    return audio_stream
