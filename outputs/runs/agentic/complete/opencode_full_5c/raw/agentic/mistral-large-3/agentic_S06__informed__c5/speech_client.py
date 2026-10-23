from typing import Optional, Dict, Any
import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError


class PollySpeechClient:
    """Amazon Polly client helper for text-to-speech operations."""

    def __init__(self):
        self.client = boto3.client(
            "polly",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

    def synthesize(
        self, text: str, voice_id: str, text_type: str = "text", **kwargs
    ) -> bytes:
        """Synthesize text or SSML to audio bytes using Amazon Polly."""
        try:
            response = self.client.synthesize_speech(
                Text=text,
                TextType=text_type,
                VoiceId=voice_id,
                OutputFormat="mp3",
                Engine="neural",
                **kwargs,
            )
            return response["AudioStream"].read()
        except (BotoCoreError, ClientError) as e:
            raise Exception(f"Amazon Polly synthesis failed: {str(e)}")

    def list_voices(self, language_code: Optional[str] = None) -> Dict[str, Any]:
        """List available voices for a target locale."""
        try:
            params = {}
            if language_code:
                params["LanguageCode"] = language_code
            response = self.client.describe_voices(**params)
            return response
        except (BotoCoreError, ClientError) as e:
            raise Exception(f"Amazon Polly voice listing failed: {str(e)}")
