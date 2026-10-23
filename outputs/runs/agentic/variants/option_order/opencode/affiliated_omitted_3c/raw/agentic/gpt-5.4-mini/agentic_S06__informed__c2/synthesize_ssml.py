from typing import Optional

from speech_client import make_polly_client


def synthesize_ssml(
    ssml: str, voice: Optional[str] = None, output_format: str = "mp3"
) -> bytes:
    client = make_polly_client()
    response = client.synthesize_speech(
        Text=ssml,
        TextType="ssml",
        OutputFormat=output_format,
        VoiceId=voice or "Joanna",
    )
    return response["AudioStream"].read()
