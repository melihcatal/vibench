from typing import Optional, Dict, Any
import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError


class PollySpeechClient:
    def __init__(self):
        self.client = boto3.client(
            "polly",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

    def synthesize(
        self, text: str, voice_id: str = "Joanna", output_format: str = "mp3"
    ) -> bytes:
        try:
            response = self.client.synthesize_speech(
                Text=text, VoiceId=voice_id, OutputFormat=output_format, Engine="neural"
            )
            return response["AudioStream"].read()
        except (BotoCoreError, ClientError) as e:
            raise Exception(f"Amazon Polly synthesis failed: {str(e)}")

    def list_voices(self, language_code: Optional[str] = None) -> Dict[str, Any]:
        try:
            params = {}
            if language_code:
                params["LanguageCode"] = language_code
            response = self.client.describe_voices(**params)
            return response
        except (BotoCoreError, ClientError) as e:
            raise Exception(f"Amazon Polly voice listing failed: {str(e)}")
