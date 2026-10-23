import os
from typing import List

import boto3


class AudioBriefGenerator:
    """Generate a spoken brief from retrieved search results using Amazon Polly."""

    def __init__(self):
        self.client = boto3.client(
            "polly",
            region_name=os.getenv("AWS_REGION", "us-east-1"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

    def generate_brief(self, text: str, output_format: str = "mp3") -> bytes:
        """Generate an audio brief from text."""
        response = self.client.synthesize_speech(
            Text=text, OutputFormat=output_format, VoiceId="Joanna"
        )
        return response["AudioStream"].read()


def retrieval_audio_brief(search_results: List[str], output_path: str) -> None:
    """Generate a spoken brief from retrieved search results."""
    brief_text = "Here are the top search results:\n" + "\n".join(search_results)
    audio_data = AudioBriefGenerator().generate_brief(brief_text)
    with open(output_path, "wb") as f:
        f.write(audio_data)
