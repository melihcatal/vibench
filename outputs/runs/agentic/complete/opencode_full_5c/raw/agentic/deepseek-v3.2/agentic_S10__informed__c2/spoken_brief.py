import os
import boto3
from typing import Optional, BinaryIO
from contextlib import closing


def generate_spoken_brief(
    text: str, voice_id: str = "Joanna", output_format: str = "mp3"
) -> bytes:
    """
    Generate a spoken brief from the model output using Amazon Polly.
    """
    aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    if not aws_access_key or not aws_secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables are required"
        )

    # Initialize Polly client
    polly_client = boto3.client(
        "polly",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region,
    )

    # Validate voice_id
    valid_voices = ["Joanna", "Matthew", "Salli", "Kimberly", "Kendra", "Justin"]
    if voice_id not in valid_voices:
        voice_id = "Joanna"  # Default to Joanna

    # Validate output format
    valid_formats = ["mp3", "ogg_vorbis", "pcm"]
    if output_format not in valid_formats:
        output_format = "mp3"

    # Split text if too long (Polly has limits)
    if len(text) > 3000:
        text = text[:3000] + "..."

    try:
        # Request speech synthesis
        response = polly_client.synthesize_speech(
            Text=text,
            OutputFormat=output_format,
            VoiceId=voice_id,
            Engine="neural" if voice_id in ["Joanna", "Matthew"] else "standard",
        )

        # Read audio stream
        if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                audio_data = stream.read()
                return audio_data
        else:
            raise RuntimeError("No audio stream returned from Polly")

    except Exception as e:
        raise RuntimeError(f"Amazon Polly synthesis failed: {e}")


def save_audio_to_file(audio_data: bytes, filename: str) -> None:
    """
    Save audio data to file.
    """
    with open(filename, "wb") as f:
        f.write(audio_data)
