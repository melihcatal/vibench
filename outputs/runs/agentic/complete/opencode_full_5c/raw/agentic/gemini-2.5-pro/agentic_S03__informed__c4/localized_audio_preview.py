import os
import boto3
from typing import Optional


def localized_audio_preview(text: str, language_code: str) -> Optional[bytes]:
    """
    Generates a spoken audio preview of translated copy using Amazon Polly.

    Args:
        text: The text to synthesize.
        language_code: The BCP-47 language code for Polly (e.g., 'en-US', 'es-ES').

    Returns:
        The audio stream as bytes, or None if an error occurs.
    """
    voice_map = {
        "en-US": "Joanna",
        "en-GB": "Amy",
        "es-ES": "Lucia",
        "fr-FR": "Celine",
        "de-DE": "Marlene",
        "it-IT": "Carla",
        "ja-JP": "Mizuki",
        "pt-BR": "Camila",
        "ru-RU": "Tatyana",
        "cmn-CN": "Zhiyu",
    }

    voice_id = voice_map.get(language_code)
    if not voice_id:
        print(f"Warning: No voice ID mapped for language code: {language_code}")
        return None

    try:
        polly_client = boto3.Session(
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        ).client("polly")

        response = polly_client.synthesize_speech(
            VoiceId=voice_id, OutputFormat="mp3", Text=text, Engine="neural"
        )

        if "AudioStream" in response:
            return response["AudioStream"].read()
        return None
    except Exception as e:
        print(f"Error calling Amazon Polly: {e}")
        return None
