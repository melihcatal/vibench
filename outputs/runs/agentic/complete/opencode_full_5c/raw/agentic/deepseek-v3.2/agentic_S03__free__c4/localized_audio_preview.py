import os
import boto3
from typing import Optional


def generate_spoken_preview(
    text: str, language_code: str = "es-ES", voice_id: Optional[str] = None
) -> dict:
    """Generate spoken previews of translated copy using Amazon Polly."""
    polly_client = boto3.client(
        "polly",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

    if not voice_id:
        voice_map = {
            "es-ES": "Lucia",
            "es-US": "Lupe",
            "en-US": "Joanna",
            "en-GB": "Amy",
            "fr-FR": "Celine",
            "de-DE": "Vicki",
            "it-IT": "Bianca",
            "pt-BR": "Camila",
            "ja-JP": "Mizuki",
        }
        voice_id = voice_map.get(language_code, "Lucia")

    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat="mp3",
        VoiceId=voice_id,
        Engine="neural",
        LanguageCode=language_code,
    )

    audio_stream = response["AudioStream"].read()

    return {
        "text": text,
        "language_code": language_code,
        "voice_id": voice_id,
        "audio_format": "mp3",
        "audio_size_bytes": len(audio_stream),
        "engine": "neural",
        "provider": "Amazon Polly",
    }
