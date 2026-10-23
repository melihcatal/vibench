import os
from typing import Dict, Any, Optional
import boto3
from botocore.exceptions import ClientError
import tempfile


def generate_spoken_briefing(
    text: str,
    voice_id: str = "Joanna",
    output_format: str = "mp3",
    language_code: str = "en-US",
) -> Dict[str, Any]:
    """Generate spoken briefings from platform outputs using Amazon Polly."""

    # Initialize AWS Polly client
    polly_client = boto3.client(
        "polly",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    try:
        # Synthesize speech using Amazon Polly
        response = polly_client.synthesize_speech(
            Text=text,
            OutputFormat=output_format,
            VoiceId=voice_id,
            LanguageCode=language_code,
            Engine="neural",  # Use neural engine for better quality
        )

        # Create temporary file for audio output
        with tempfile.NamedTemporaryFile(
            suffix=f".{output_format}", delete=False
        ) as temp_file:
            # Write audio stream to file
            if "AudioStream" in response:
                audio_stream = response["AudioStream"]
                temp_file.write(audio_stream.read())
                temp_file_path = temp_file.name
            else:
                raise ValueError("No audio stream in response")

        # Get speech marks if requested (for synchronization)
        speech_marks_response = polly_client.synthesize_speech(
            Text=text,
            OutputFormat="json",
            VoiceId=voice_id,
            LanguageCode=language_code,
            SpeechMarkTypes=["sentence", "word"],
            Engine="neural",
        )

        speech_marks = None
        if "AudioStream" in speech_marks_response:
            speech_marks = speech_marks_response["AudioStream"].read().decode("utf-8")

        # Get voice metadata
        voices_response = polly_client.describe_voices(LanguageCode=language_code)
        voice_metadata = None
        for voice in voices_response["Voices"]:
            if voice["Id"] == voice_id:
                voice_metadata = voice
                break

        return {
            "provider": "amazon-polly",
            "service": "SynthesizeSpeech",
            "audio_file_path": temp_file_path,
            "output_format": output_format,
            "voice_id": voice_id,
            "language_code": language_code,
            "text_length": len(text),
            "character_count": len(text),
            "engine": "neural",
            "speech_marks": speech_marks,
            "voice_metadata": voice_metadata,
            "request_id": response.get("ResponseMetadata", {}).get("RequestId", ""),
        }

    except ClientError as e:
        print(f"Amazon Polly error: {e}")

        # Create empty placeholder file
        with tempfile.NamedTemporaryFile(
            suffix=f".{output_format}", delete=False
        ) as temp_file:
            temp_file_path = temp_file.name

        return {
            "provider": "fallback-placeholder",
            "service": "placeholder-audio",
            "audio_file_path": temp_file_path,
            "output_format": output_format,
            "voice_id": voice_id,
            "language_code": language_code,
            "text_length": len(text),
            "error": str(e),
            "warning": "Amazon Polly service unavailable, created placeholder file",
        }


def get_available_voices(language_code: str = "en-US") -> List[Dict[str, Any]]:
    """Get available voices from Amazon Polly."""

    polly_client = boto3.client(
        "polly",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    try:
        response = polly_client.describe_voices(LanguageCode=language_code)

        voices = []
        for voice in response["Voices"]:
            voices.append(
                {
                    "id": voice["Id"],
                    "name": voice["Name"],
                    "language_code": voice["LanguageCode"],
                    "language_name": voice["LanguageName"],
                    "gender": voice["Gender"],
                    "supported_engines": voice.get("SupportedEngines", []),
                    "additional_language_codes": voice.get(
                        "AdditionalLanguageCodes", []
                    ),
                }
            )

        return voices

    except ClientError as e:
        print(f"Error getting available voices: {e}")

        # Return common voices as fallback
        return [
            {
                "id": "Joanna",
                "name": "Joanna",
                "language_code": "en-US",
                "language_name": "US English",
                "gender": "Female",
                "supported_engines": ["neural", "standard"],
            },
            {
                "id": "Matthew",
                "name": "Matthew",
                "language_code": "en-US",
                "language_name": "US English",
                "gender": "Male",
                "supported_engines": ["neural", "standard"],
            },
            {
                "id": "Ivy",
                "name": "Ivy",
                "language_code": "en-US",
                "language_name": "US English",
                "gender": "Female",
                "supported_engines": ["neural", "standard"],
            },
        ]


def generate_briefing_with_ssml(
    text: str, ssml_tags: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Generate spoken briefing with SSML markup for enhanced control."""

    polly_client = boto3.client(
        "polly",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    # Create SSML with optional tags
    if ssml_tags:
        ssml_text = f"<speak>"
        if "break" in ssml_tags:
            ssml_text += f"<break time='{ssml_tags['break']}s'/>"
        if "emphasis" in ssml_tags:
            ssml_text += f"<emphasis level='{ssml_tags['emphasis']}'>"

        ssml_text += text

        if "emphasis" in ssml_tags:
            ssml_text += "</emphasis>"
        if "prosody" in ssml_tags:
            ssml_text += f"<prosody rate='{ssml_tags['prosody']}'>"
            ssml_text += text
            ssml_text += "</prosody>"

        ssml_text += "</speak>"
    else:
        # Basic SSML wrapper
        ssml_text = f"<speak>{text}</speak>"

    try:
        response = polly_client.synthesize_speech(
            Text=ssml_text,
            OutputFormat="mp3",
            VoiceId="Joanna",
            LanguageCode="en-US",
            Engine="neural",
            TextType="ssml",
        )

        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
            if "AudioStream" in response:
                audio_stream = response["AudioStream"]
                temp_file.write(audio_stream.read())
                temp_file_path = temp_file.name

        return {
            "provider": "amazon-polly",
            "service": "SynthesizeSpeech",
            "text_type": "ssml",
            "audio_file_path": temp_file_path,
            "output_format": "mp3",
            "voice_id": "Joanna",
            "language_code": "en-US",
            "ssml_used": True,
            "ssml_tags": ssml_tags,
            "request_id": response.get("ResponseMetadata", {}).get("RequestId", ""),
        }

    except ClientError as e:
        print(f"Amazon Polly SSML error: {e}")

        # Fallback to regular text synthesis
        return generate_spoken_briefing(text, "Joanna", "mp3", "en-US")
