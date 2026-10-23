from typing import Optional

from speech_client import make_polly_client
from speech_models import normalize_text


def synthesize_text(
    text: str, voice: Optional[str] = None, output_format: str = "mp3"
) -> bytes:
    client = make_polly_client()
    response = client.synthesize_speech(
        Text=normalize_text(text), OutputFormat=output_format, VoiceId=voice or "Joanna"
    )
    return response["AudioStream"].read()
