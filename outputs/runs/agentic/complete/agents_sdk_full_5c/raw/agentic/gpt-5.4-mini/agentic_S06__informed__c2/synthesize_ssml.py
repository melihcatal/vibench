from __future__ import annotations

from typing import Optional

from speech_client import create_polly_client, load_config
from speech_models import SpeechRequest, SpeechResponse, ssml_wrap


def synthesize_ssml(text: str, voice_name: Optional[str] = None, locale: Optional[str] = None, pitch: Optional[str] = None, rate: Optional[str] = None) -> bytes:
    prosody = {k: v for k, v in {"pitch": pitch, "rate": rate}.items() if v is not None}
    ssml = ssml_wrap(text, voice_name=voice_name, prosody=prosody)
    request = SpeechRequest(text=ssml, voice_name=voice_name, locale=locale, ssml=True, prosody=prosody)
    client = create_polly_client(load_config())
    response = client.synthesize_speech(
        Text=request.text,
        TextType="ssml",
        VoiceId=request.voice_name or "Joanna",
        OutputFormat="mp3",
    )
    audio_stream = response["AudioStream"].read()
    SpeechResponse(audio=audio_stream, provider="amazon-polly", metadata={"request": request.__dict__})
    return audio_stream
