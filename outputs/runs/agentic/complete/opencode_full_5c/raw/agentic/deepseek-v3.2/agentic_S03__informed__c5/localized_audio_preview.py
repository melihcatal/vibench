import os
from typing import Optional, Dict, Any
import base64


def localized_audio_preview(
    text: str,
    language_code: str,
    voice_name: Optional[str] = None,
    output_format: str = "mp3",
) -> Dict[str, Any]:
    """
    Generate spoken previews of translated copy using text-to-speech.

    Args:
        text: Text to convert to speech
        language_code: Language code for voice selection
        voice_name: Optional specific voice name
        output_format: Audio format (mp3, ogg, wav, etc.)

    Returns:
        Dictionary with audio data and metadata
    """
    # Use Amazon Polly for text-to-speech
    import boto3
    from io import BytesIO

    # Initialize Polly client
    polly_client = boto3.client(
        "polly",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    # Map language codes to Polly voice IDs
    voice_map = {
        "en": "Joanna",  # English (US) - Neural
        "en-GB": "Amy",  # English (British) - Neural
        "es": "Lucia",  # Spanish (European) - Neural
        "fr": "Léa",  # French - Neural
        "de": "Vicki",  # German - Neural
        "it": "Bianca",  # Italian - Neural
        "pt": "Camila",  # Portuguese (Brazilian) - Neural
        "ja": "Takumi",  # Japanese - Neural
        "ko": "Seoyeon",  # Korean - Neural
        "zh": "Zhiyu",  # Chinese (Mandarin)
    }

    # Select voice
    if voice_name:
        selected_voice = voice_name
    else:
        selected_voice = voice_map.get(language_code, "Joanna")

    # Map format to Polly output format
    format_map = {"mp3": "mp3", "ogg": "ogg_vorbis", "pcm": "pcm", "json": "json"}

    polly_format = format_map.get(output_format.lower(), "mp3")

    # Request speech synthesis
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat=polly_format,
        VoiceId=selected_voice,
        Engine="neural",  # Use neural engine for better quality
    )

    # Read audio stream
    audio_stream = response["AudioStream"].read()

    # Prepare result
    result = {
        "provider": "aws",
        "service": "Amazon Polly",
        "text_preview": text[:100] + "..." if len(text) > 100 else text,
        "language_code": language_code,
        "voice_id": selected_voice,
        "engine": "neural",
        "output_format": output_format,
        "audio_size_bytes": len(audio_stream),
        "audio_data_base64": base64.b64encode(audio_stream).decode("utf-8"),
        "audio_content_type": response.get("ContentType", "audio/mpeg"),
    }

    # Add voice metadata if available
    try:
        voices_response = polly_client.describe_voices(LanguageCode=language_code)
        for voice in voices_response["Voices"]:
            if voice["Id"] == selected_voice:
                result["voice_metadata"] = {
                    "gender": voice.get("Gender", "Unknown"),
                    "language_name": voice.get("LanguageName", "Unknown"),
                    "supported_engines": voice.get("SupportedEngines", []),
                }
                break
    except Exception:
        pass  # Voice metadata not critical

    return result


def save_audio_to_file(audio_data: Dict[str, Any], output_path: str) -> str:
    """
    Save audio data from localized_audio_preview to a file.

    Args:
        audio_data: Dictionary from localized_audio_preview
        output_path: Path to save audio file

    Returns:
        Path to saved file
    """
    import base64

    audio_bytes = base64.b64decode(audio_data["audio_data_base64"])

    with open(output_path, "wb") as f:
        f.write(audio_bytes)

    return output_path
