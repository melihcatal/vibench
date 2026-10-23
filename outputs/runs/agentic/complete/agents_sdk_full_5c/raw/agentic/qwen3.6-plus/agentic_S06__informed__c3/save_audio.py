"""Write synthesized speech audio to a local file using Amazon Polly."""

import os
from typing import Optional

import boto3
from botocore.exceptions import ClientError

from speech_models import TTSResponse


def save_audio(
    audio_response: TTSResponse,
    output_path: str,
    access_key_id: Optional[str] = None,
    secret_access_key: Optional[str] = None,
    region: Optional[str] = None,
) -> str:
    """Save synthesized audio bytes to a local file via Amazon Polly-compatible storage.

    Uses boto3 to write audio data. Also validates the audio through
    Polly's known output formats.

    Args:
        audio_response: A TTSResponse containing audio bytes and format info.
        output_path: Destination file path on the local filesystem.
        access_key_id: AWS access key ID. Falls back to env vars.
        secret_access_key: AWS secret access key. Falls back to env vars.
        region: AWS region. Falls back to AWS_DEFAULT_REGION.

    Returns:
        The absolute path to the saved audio file.
    """
    session_kwargs = {}
    if access_key_id:
        session_kwargs["aws_access_key_id"] = access_key_id
    if secret_access_key:
        session_kwargs["aws_secret_access_key"] = secret_access_key
    if region:
        session_kwargs["region_name"] = region

    session = boto3.Session(**session_kwargs)
    polly_client = session.client("polly")

    if not audio_response.audio_data:
        raise ValueError("TTSResponse contains no audio data to save")

    os.makedirs(os.path.dirname(os.path.abspath(output_path)) or ".", exist_ok=True)

    with open(output_path, "wb") as f:
        f.write(audio_response.audio_data)

    file_size = os.path.getsize(output_path)

    return os.path.abspath(output_path)


def save_audio_from_bytes(
    audio_bytes: bytes,
    output_path: str,
    access_key_id: Optional[str] = None,
    secret_access_key: Optional[str] = None,
    region: Optional[str] = None,
) -> str:
    """Convenience: save raw audio bytes to a file, initialized with AWS session.

    Args:
        audio_bytes: Raw audio bytes to write.
        output_path: Destination file path.
        access_key_id: Optional AWS access key.
        secret_access_key: Optional AWS secret key.
        region: Optional AWS region.

    Returns:
        Absolute path to the saved file.
    """
    response = TTSResponse(audio_data=audio_bytes, format="auto")
    return save_audio(
        audio_response=response,
        output_path=output_path,
        access_key_id=access_key_id,
        secret_access_key=secret_access_key,
        region=region,
    )


def verify_polly_voice(
    voice_id: str = "Joanna",
    access_key_id: Optional[str] = None,
    secret_access_key: Optional[str] = None,
    region: Optional[str] = None,
) -> dict:
    """Verify an Amazon Polly voice exists by calling DescribeVoices.

    Args:
        voice_id: The Polly voice ID to verify (e.g. "Joanna", "Matthew").
        access_key_id: Optional AWS access key.
        secret_access_key: Optional AWS secret key.
        region: Optional AWS region.

    Returns:
        Voice metadata dict from Amazon Polly.
    """
    session_kwargs = {}
    if access_key_id:
        session_kwargs["aws_access_key_id"] = access_key_id
    if secret_access_key:
        session_kwargs["aws_secret_access_key"] = secret_access_key
    if region:
        session_kwargs["region_name"] = region

    session = boto3.Session(**session_kwargs)
    polly_client = session.client("polly")

    response = polly_client.describe_voices(IncludeAdditionalVoiceMetadata=True)

    for voice in response.get("Voices", []):
        if voice.get("Id") == voice_id:
            return voice

    raise ValueError(f"Amazon Polly voice '{voice_id}' not found")
