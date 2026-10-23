import os
from typing import Optional
import boto3
from botocore.exceptions import BotoCoreError, ClientError


def generate_spoken_preview(
    text: str,
    language_code: str = "es-ES",
    voice_id: str = "Lucia",
    output_format: str = "mp3",
) -> Optional[bytes]:
    """
    Generate spoken previews of translated copy using Amazon Polly.

    Args:
        text: Text to convert to speech
        language_code: Language and locale code (default: "es-ES" for Spanish Spain)
        voice_id: Polly voice ID to use (default: "Lucia" for Spanish female)
        output_format: Output audio format (mp3, ogg_vorbis, pcm)

    Returns:
        Audio bytes if successful, None otherwise
    """
    polly_client = boto3.client(
        "polly",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

    try:
        response = polly_client.synthesize_speech(
            Text=text,
            OutputFormat=output_format,
            VoiceId=voice_id,
            LanguageCode=language_code,
            Engine="neural" if language_code.startswith("en") else "standard",
        )

        if "AudioStream" in response:
            audio_data = response["AudioStream"].read()
            return audio_data
        else:
            return None

    except (BotoCoreError, ClientError) as error:
        print(f"Error generating speech: {error}")
        return None


def list_available_voices(language_code: Optional[str] = None) -> list:
    """
    List available Amazon Polly voices for a language.

    Args:
        language_code: Optional language code filter

    Returns:
        List of available voices
    """
    polly_client = boto3.client(
        "polly",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

    params = {}
    if language_code:
        params["LanguageCode"] = language_code

    response = polly_client.describe_voices(**params)

    voices = []
    for voice in response["Voices"]:
        voices.append(
            {
                "id": voice["Id"],
                "language_code": voice["LanguageCode"],
                "language_name": voice["LanguageName"],
                "gender": voice["Gender"],
                "supported_engines": voice.get("SupportedEngines", []),
            }
        )

    return voices
