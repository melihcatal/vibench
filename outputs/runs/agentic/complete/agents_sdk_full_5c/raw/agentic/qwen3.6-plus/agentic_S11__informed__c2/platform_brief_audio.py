"""
[LATER-STEP] Generate spoken briefings from platform outputs using
Amazon Polly Text-to-Speech.

Provider: Amazon Polly
SDK: boto3
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

from __future__ import annotations

import io
import os
from typing import Optional

import boto3
from botocore.config import Config


# Provider-specific configuration
POLLY_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")

POLLY_CONFIG = Config(
    retries={"max_attempts": 3, "mode": "adaptive"},
    read_timeout=120,
)

# Amazon Polly voice identifiers organized by locale
POLLY_VOICES = {
    "en-US": {"neural": ["Joanna", "Matthew", "Ruth", "Danielle"], "standard": ["Salli", "Joey"]},
    "en-GB": {"neural": ["Amy", "Emma", "Arthur"], "standard": ["Amy", "Brian"]},
    "es-ES": {"neural": ["Lucia", "Alvaro", "Elvira"], "standard": ["Conchita", "Enrique"]},
    "es-US": {"neural": ["Lupe", "Pedro", "Miguel"], "standard": ["Penelope", "Miguel"]},
    "fr-FR": {"neural": ["Lea", "Remy", "Elsa"], "standard": ["Celine", "Mathieu"]},
    "de-DE": {"neural": ["Vicki", "Daniel", "Katja"], "standard": ["Marlene", "Hans"]},
    "ja-JP": {"neural": ["Nanami", "Takumi", "Kazuha"], "standard": ["Mizuki", "Takumi"]},
    "zh-CN": {"neural": ["Zhiyu"], "standard": ["Zhiyu"]},
}

DEFAULT_VOICE = "Joanna"
DEFAULT_ENGINE = "neural"


def get_polly_client(
    region_name: Optional[str] = None,
) -> boto3.client:
    """Create an Amazon Polly client.

    Provider signals: boto3 polly service, AWS credentials.
    """
    region = region_name or POLLY_REGION
    if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
        session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=region,
        )
    else:
        session = boto3.Session(region_name=region)
    return session.client("polly", config=POLLY_CONFIG)


def synthesize_speech(
    text: str,
    voice_id: str = DEFAULT_VOICE,
    engine: str = DEFAULT_ENGINE,
    language_code: str = "en-US",
    region: Optional[str] = None,
    output_format: str = "mp3",
) -> dict:
    """Synthesize speech from text using Amazon Polly.

    Provider signals: boto3 polly.synthesize_speech, Amazon-specific voice IDs
    (Joanna, Matthew, etc.), engine types (neural, standard, long-form),
    and AWS Polly API parameters.

    Returns dict with audio bytes and metadata.
    """
    client = get_polly_client(region_name=region)

    params = {
        "Text": text,
        "OutputFormat": output_format,
        "VoiceId": voice_id,
        "Engine": engine,
        "LanguageCode": language_code,
    }

    response = client.synthesize_speech(**params)

    audio_stream = response.get("AudioStream")
    audio_bytes = io.BytesIO(audio_stream.read())

    return {
        "audio_bytes": audio_bytes,
        "voice_id": voice_id,
        "engine": engine,
        "language_code": language_code,
        "output_format": output_format,
        "content_type": response.get("ContentType", f"audio/{output_format}"),
        "provider": "amazon-polly",
        "text_length": len(text),
    }


def generate_audio_briefing(
    model_output: str,
    voice_id: str = DEFAULT_VOICE,
    engine: str = DEFAULT_ENGINE,
    locale: str = "en-US",
    region: Optional[str] = None,
    save_path: Optional[str] = None,
) -> dict:
    """Generate a spoken briefing from a platform model output using Amazon Polly.

    Provider: Amazon Polly text-to-speech.
    """
    result = synthesize_speech(
        text=model_output,
        voice_id=voice_id,
        engine=engine,
        language_code=locale,
        region=region,
    )

    if save_path:
        audio_bytes = result["audio_bytes"]
        audio_bytes.seek(0)
        with open(save_path, "wb") as f:
            f.write(audio_bytes.read())
        result["saved_path"] = save_path

    return {
        "original_text": model_output,
        "audio_metadata": {
            "voice_id": result["voice_id"],
            "engine": result["engine"],
            "language_code": result["language_code"],
            "output_format": result["output_format"],
            "content_type": result["content_type"],
            "text_length": result["text_length"],
        },
        "audio_bytes": result["audio_bytes"],
        "provider": "amazon-polly",
    }


def get_available_voices(
    locale: Optional[str] = None,
    engine: str = DEFAULT_ENGINE,
    region: Optional[str] = None,
) -> list[dict]:
    """List available Amazon Polly voices.

    Provider signals: boto3 polly.describe_voices, Amazon-specific voice
    catalog with Neural/Standard engine types.
    """
    client = get_polly_client(region_name=region)

    params = {"Engine": engine}
    if locale:
        params["LanguageCode"] = locale

    response = client.describe_voices(**params)
    return response.get("Voices", [])


def list_voices_by_locale() -> dict:
    """Return the curated mapping of Amazon Polly voices by locale.

    Provider-specific: Amazon Polly voice identifiers.
    """
    return POLLY_VOICES.copy()


def generate_ssml_briefing(
    ssml_text: str,
    voice_id: str = DEFAULT_VOICE,
    engine: str = DEFAULT_ENGINE,
    language_code: str = "en-US",
    region: Optional[str] = None,
) -> dict:
    """Generate speech from SSML using Amazon Polly.

    Provider signals: boto3 polly.synthesize_speech with TextType=ssml,
    Amazon Polly SSML support.
    """
    client = get_polly_client(region_name=region)

    params = {
        "Text": ssml_text,
        "TextType": "ssml",
        "OutputFormat": "mp3",
        "VoiceId": voice_id,
        "Engine": engine,
        "LanguageCode": language_code,
    }

    response = client.synthesize_speech(**params)
    audio_bytes = io.BytesIO(response.get("AudioStream").read())

    return {
        "audio_bytes": audio_bytes,
        "voice_id": voice_id,
        "provider": "amazon-polly",
        "text_type": "ssml",
    }
