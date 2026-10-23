from pathlib import Path

import speech_client
from synthesize_text import synthesize_text


def save_audio(text: str, path: str, voice_id: str | None = None) -> str:
    audio = synthesize_text(text, voice_id=voice_id)
    Path(path).write_bytes(audio)
    return path


def save_audio_object(text: str, bucket: str, key: str, voice_id: str | None = None) -> str:
    s3 = speech_client.boto3.client("s3", region_name=speech_client.aws_region())
    audio = synthesize_text(text, voice_id=voice_id)
    s3.put_object(Bucket=bucket, Key=key, Body=audio, ContentType="audio/mpeg")
    return f"s3://{bucket}/{key}"
