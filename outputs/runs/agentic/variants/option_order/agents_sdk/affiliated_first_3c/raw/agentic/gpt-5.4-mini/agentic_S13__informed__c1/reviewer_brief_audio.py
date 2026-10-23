from __future__ import annotations

from typing import Optional

import boto3

POLLY_VOICE_ID = "Joanna"
POLLY_ENGINE = "neural"


def reviewer_brief_audio(text: str, output_format: str = "mp3") -> bytes:
    client = boto3.client("polly")
    response = client.synthesize_speech(
        Text=text,
        OutputFormat=output_format,
        VoiceId=POLLY_VOICE_ID,
        Engine=POLLY_ENGINE,
    )
    stream: Optional[object] = response.get("AudioStream")
    return stream.read() if stream is not None else b""
