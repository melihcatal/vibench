import boto3
import os
from typing import Dict, Any, Optional
from contextlib import closing


def generate_spoken_preview(
    text: str, language_code: str, voice_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate spoken previews of translated copy using Amazon Polly.

    Args:
        text: Text to convert to speech
        language_code: Language code for voice selection
        voice_id: Specific voice ID to use (optional)

    Returns:
        Dictionary with audio information and metadata
    """
    polly_client = boto3.client(
        "polly",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

    if not voice_id:
        voice_id = get_default_voice_for_language(language_code)

    try:
        response = polly_client.synthesize_speech(
            Text=text, OutputFormat="mp3", VoiceId=voice_id, Engine="neural"
        )

        if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                audio_data = stream.read()

                return {
                    "text": text,
                    "language_code": language_code,
                    "voice_id": voice_id,
                    "audio_format": "mp3",
                    "audio_size_bytes": len(audio_data),
                    "engine": "neural",
                    "provider": "Amazon Polly",
                    "audio_data": audio_data,
                }
        else:
            raise Exception("No audio stream in response")

    except Exception as e:
        return {
            "text": text,
            "language_code": language_code,
            "voice_id": voice_id,
            "error": str(e),
            "provider": "Amazon Polly",
        }


def get_default_voice_for_language(language_code: str) -> str:
    """
    Get default voice ID for a language code.

    Args:
        language_code: Language code

    Returns:
        Voice ID string
    """
    voice_mapping = {
        "en": "Joanna",  # English (US) - Neural female
        "en-GB": "Amy",  # English (British) - Neural female
        "es": "Lucia",  # Spanish - Neural female
        "fr": "Lea",  # French - Neural female
        "de": "Vicki",  # German - Neural female
        "it": "Bianca",  # Italian - Neural female
        "pt": "Camila",  # Portuguese (Brazilian) - Neural female
        "ja": "Takumi",  # Japanese - Neural male
        "ko": "Seoyeon",  # Korean - Neural female
        "zh": "Zhiyu",  # Chinese (Mandarin) - Neural female
    }

    return voice_mapping.get(language_code, "Joanna")


def list_available_voices(language_code: Optional[str] = None) -> list:
    """
    List available voices from Amazon Polly.

    Args:
        language_code: Filter by language code (optional)

    Returns:
        List of available voices
    """
    polly_client = boto3.client(
        "polly",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

    response = polly_client.describe_voices()

    voices = response.get("Voices", [])

    if language_code:
        voices = [v for v in voices if v.get("LanguageCode") == language_code]

    return voices
