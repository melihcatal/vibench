import os
from typing import Optional
import boto3
from botocore.exceptions import ClientError


class TextToSpeechClient:
    """Client for converting text to speech using Amazon Polly."""

    def __init__(
        self,
        aws_access_key: str = None,
        aws_secret_key: str = None,
        region: str = "us-east-1",
    ):
        self.aws_access_key = aws_access_key or os.environ.get("AWS_ACCESS_KEY_ID")
        self.aws_secret_key = aws_secret_key or os.environ.get("AWS_SECRET_ACCESS_KEY")
        self.region = region

        if not self.aws_access_key or not self.aws_secret_key:
            raise ValueError("AWS credentials not found in environment variables")

        self.client = boto3.client(
            "polly",
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
            region_name=self.region,
        )

    def synthesize_speech(
        self, text: str, voice_id: str = "Joanna", output_format: str = "mp3"
    ) -> bytes:
        """Convert text to speech."""
        try:
            response = self.client.synthesize_speech(
                Text=text,
                OutputFormat=output_format,
                VoiceId=voice_id,
                Engine="neural",  # Use neural engine for better quality
            )

            if "AudioStream" in response:
                return response["AudioStream"].read()
            else:
                raise RuntimeError("No audio stream in response")

        except ClientError as e:
            raise RuntimeError(f"AWS Polly error: {str(e)}")

    def list_available_voices(self) -> list:
        """List available voices."""
        try:
            response = self.client.describe_voices()
            return [voice["Id"] for voice in response["Voices"]]
        except ClientError as e:
            raise RuntimeError(f"Failed to list voices: {str(e)}")


def generate_spoken_brief(text: str, output_file: Optional[str] = None) -> bytes:
    """
    Generate a spoken brief from model output using Amazon Polly.
    """
    client = TextToSpeechClient()

    # Truncate text if too long for Polly (3000 character limit)
    if len(text) > 3000:
        text = text[:2997] + "..."

    audio_data = client.synthesize_speech(
        text=text,
        voice_id="Joanna",  # Female US English voice
        output_format="mp3",
    )

    if output_file:
        with open(output_file, "wb") as f:
            f.write(audio_data)

    return audio_data


def generate_spoken_summary(text: str, max_length: int = 1500) -> bytes:
    """
    Generate a spoken summary from longer text.
    """
    # First summarize if text is too long
    if len(text) > max_length:
        # Simple truncation for demo - in production, use proper summarization
        summary = text[:max_length] + "... (truncated)"
    else:
        summary = text

    client = TextToSpeechClient()

    # Add a brief introduction
    spoken_text = f"Here is a brief summary: {summary}"

    return client.synthesize_speech(
        text=spoken_text,
        voice_id="Matthew",  # Male US English voice
        output_format="mp3",
    )


def get_available_voices() -> list:
    """Get list of available voices from Amazon Polly."""
    client = TextToSpeechClient()
    return client.list_available_voices()
