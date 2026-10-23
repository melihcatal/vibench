import boto3
import os
from typing import List

class PollyClient:
    def __init__(self, region_name=None):
        self.region_name = region_name or os.environ.get("AWS_REGION", "us-east-1")
        self.client = boto3.client("polly", region_name=self.region_name)

    def synthesize_speech(self, text: str, voice_id: str = 'Joanna', output_format: str = 'mp3') -> bytes:
        """Synthesizes speech from text using AWS Polly.

        Args:
            text: The text to convert to speech.
            voice_id: The ID of the voice to use (e.g., 'Joanna', 'Matthew').
            output_format: The output format of the audio (e.g., 'mp3', 'ogg_vorbis', 'pcm').

        Returns:
            The audio stream as bytes.
        """
        response = self.client.synthesize_speech(
            Text=text,
            OutputFormat=output_format,
            VoiceId=voice_id
        )
        return response['AudioStream'].read()

def retrieval_audio_brief(retrieved_texts: List[str], brief_title: str = "Search Results Brief") -> bytes:
    """Generates a spoken brief from retrieved search results using AWS Polly.

    Args:
        retrieved_texts: A list of text strings representing the retrieved search results.
        brief_title: An optional title for the audio brief.

    Returns:
        The audio brief as bytes (e.g., in MP3 format).
    """
    polly_client = PollyClient()
    full_brief_text = f"{brief_title}. "
    for i, text in enumerate(retrieved_texts):
        full_brief_text += f"Result {i+1}: {text}. "

    audio_bytes = polly_client.synthesize_speech(full_brief_text)
    return audio_bytes
