import io
import os
from typing import Optional

from model_client import get_polly_client
from model_models import AudioResult


POLLY_VOICE_ID = os.environ.get("POLLY_VOICE_ID", "Joanna")
POLLY_ENGINE = os.environ.get("POLLY_ENGINE", "neural")
POLLY_LANGUAGE_CODE = os.environ.get("POLLY_LANGUAGE_CODE", "en-US")


def generate_platform_brief_audio(
    text: str,
    voice_id: Optional[str] = None,
    engine: Optional[str] = None,
    language_code: Optional[str] = None,
    region: Optional[str] = None,
    output_format: str = "mp3",
    sample_rate: Optional[str] = None,
) -> AudioResult:
    vid = voice_id or POLLY_VOICE_ID
    eng = engine or POLLY_ENGINE
    lang = language_code or POLLY_LANGUAGE_CODE

    client = get_polly_client(region=region)

    kwargs = {
        "Text": text,
        "OutputFormat": output_format,
        "VoiceId": vid,
        "Engine": eng,
        "LanguageCode": lang,
    }

    if sample_rate:
        kwargs["SampleRate"] = sample_rate

    response = client.synthesize_speech(**kwargs)

    audio_stream = response.get("AudioStream").read()
    content_type = response.get("ContentType", "audio/mpeg")

    return AudioResult(
        audio_stream=audio_stream,
        content_type=content_type,
        raw_response={
            "voice_id": vid,
            "engine": eng,
            "language_code": lang,
            "output_format": output_format,
            "content_type": content_type,
            "audio_size_bytes": len(audio_stream),
        },
    )


def generate_platform_brief_audio_ssml(
    ssml: str,
    voice_id: Optional[str] = None,
    engine: Optional[str] = None,
    language_code: Optional[str] = None,
    region: Optional[str] = None,
    output_format: str = "mp3",
) -> AudioResult:
    vid = voice_id or POLLY_VOICE_ID
    eng = engine or POLLY_ENGINE
    lang = language_code or POLLY_LANGUAGE_CODE

    client = get_polly_client(region=region)

    kwargs = {
        "Text": ssml,
        "TextType": "ssml",
        "OutputFormat": output_format,
        "VoiceId": vid,
        "Engine": eng,
        "LanguageCode": lang,
    }

    response = client.synthesize_speech(**kwargs)

    audio_stream = response.get("AudioStream").read()
    content_type = response.get("ContentType", "audio/mpeg")

    return AudioResult(
        audio_stream=audio_stream,
        content_type=content_type,
        raw_response={
            "voice_id": vid,
            "engine": eng,
            "language_code": lang,
            "output_format": output_format,
            "content_type": content_type,
            "audio_size_bytes": len(audio_stream),
        },
    )
