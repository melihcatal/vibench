import os
import boto3
from typing import Dict, Any, Optional
import tempfile


def text_to_speech(
    text: str, voice_id: str = "Joanna", output_format: str = "mp3"
) -> Dict[str, Any]:
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")

    if not aws_access_key or not aws_secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables must be set"
        )

    polly_client = boto3.client(
        "polly",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region,
    )

    response = polly_client.synthesize_speech(
        Text=text, OutputFormat=output_format, VoiceId=voice_id, Engine="neural"
    )

    audio_stream = response["AudioStream"].read()

    with tempfile.NamedTemporaryFile(
        delete=False, suffix=f".{output_format}"
    ) as tmp_file:
        tmp_file.write(audio_stream)
        audio_file_path = tmp_file.name

    result = {
        "text": text,
        "voice_id": voice_id,
        "output_format": output_format,
        "audio_file_path": audio_file_path,
        "audio_size_bytes": len(audio_stream),
        "provider": "Amazon Polly",
        "engine": "neural",
    }

    return result


def list_available_voices(language_code: Optional[str] = None) -> List[Dict[str, Any]]:
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")

    if not aws_access_key or not aws_secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables must be set"
        )

    polly_client = boto3.client(
        "polly",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region,
    )

    response = polly_client.describe_voices()

    voices = []
    for voice in response["Voices"]:
        if language_code and voice["LanguageCode"] != language_code:
            continue

        voice_info = {
            "id": voice["Id"],
            "name": voice["Name"],
            "language_code": voice["LanguageCode"],
            "language_name": voice["LanguageName"],
            "gender": voice["Gender"],
            "supported_engines": voice.get("SupportedEngines", []),
        }
        voices.append(voice_info)

    return voices


def create_briefing_audio(text: str, briefing_style: str = "news") -> Dict[str, Any]:
    voice_mapping = {
        "news": "Joanna",
        "conversational": "Matthew",
        "professional": "Joey",
        "friendly": "Salli",
        "authoritative": "Stephen",
    }

    voice_id = voice_mapping.get(briefing_style, "Joanna")

    if briefing_style == "news":
        formatted_text = f"News briefing. {text}"
    elif briefing_style == "conversational":
        formatted_text = f"Here's what you need to know. {text}"
    else:
        formatted_text = text

    return text_to_speech(formatted_text, voice_id=voice_id)


def get_voice_characteristics(voice_id: str) -> Dict[str, Any]:
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")

    if not aws_access_key or not aws_secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables must be set"
        )

    polly_client = boto3.client(
        "polly",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region,
    )

    response = polly_client.describe_voices()

    for voice in response["Voices"]:
        if voice["Id"] == voice_id:
            return {
                "id": voice["Id"],
                "name": voice["Name"],
                "language_code": voice["LanguageCode"],
                "language_name": voice["LanguageName"],
                "gender": voice["Gender"],
                "supported_engines": voice.get("SupportedEngines", []),
                "additional_language_codes": voice.get("AdditionalLanguageCodes", []),
            }

    raise ValueError(f"Voice ID {voice_id} not found")
