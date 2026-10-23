"""Generate spoken briefings from platform outputs using Amazon Polly TTS.

Uses the boto3 Amazon Polly SynthesizeSpeech API to convert text
produced by a platform model into spoken audio in various voices.
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
Provider: Amazon Polly
"""

from typing import Optional

from model_client import get_polly_client
from model_models import AudioResult

DEFAULT_VOICE_ID = "Joanna"
DEFAULT_ENGINE = "neural"


def platform_brief_audio(
    text: str,
    voice_id: str = DEFAULT_VOICE_ID,
    engine: str = DEFAULT_ENGINE,
    sample_rate: str = "22050",
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
) -> AudioResult:
    """Generate spoken audio from platform model output using Amazon Polly.

    Calls the Polly SynthesizeSpeech API with the specified voice
    (default: Joanna) and neural engine to produce high-quality
    speech audio as PCM bytes.
    """
    if not text or not text.strip():
        raise ValueError("Cannot synthesize empty text")

    client = get_polly_client(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    response = client.synthesize_speech(
        Text=text,
        OutputFormat="pcm",
        VoiceId=voice_id,
        Engine=engine,
        SampleRate=sample_rate,
    )

    audio_bytes = response["AudioStream"].read()
    content_type = response.get("ContentType", "audio/pcm")

    return AudioResult(
        audio_bytes=audio_bytes,
        content_type=content_type,
        raw_response={
            "voice_id": voice_id,
            "engine": engine,
            "sample_rate": sample_rate,
            "content_type": content_type,
        },
    )


def save_audio_to_file(
    audio_result: AudioResult,
    output_path: str,
) -> str:
    """Save the Polly audio result to a PCM file."""
    with open(output_path, "wb") as f:
        f.write(audio_result.audio_bytes)
    return output_path


def generate_multilingual_brief(
    text: str,
    voice_id: str = "Lupe",
    target_language: str = "es",
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
) -> AudioResult:
    """Generate a briefing in a specific language using a regional voice.

    Uses a Spanish voice (Lupe) on Amazon Polly to synthesize
    Spanish-language platform output as spoken audio.
    """
    return platform_brief_audio(
        text=text,
        voice_id=voice_id,
        engine=DEFAULT_ENGINE,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )


if __name__ == "__main__":
    sample = "Welcome to the daily technology briefing. Today we discuss cloud computing."
    result = platform_brief_audio(sample, voice_id="Joanna")
    print(f"Audio size: {len(result.audio_bytes)} bytes")
    print(f"Content type: {result.content_type}")
    print(f"Voice: {result.raw_response.get('voice_id')}")
