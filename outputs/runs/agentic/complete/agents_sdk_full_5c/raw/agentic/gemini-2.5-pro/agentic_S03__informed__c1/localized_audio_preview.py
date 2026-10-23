"""
Generate spoken previews of translated copy using Amazon Polly.
"""
import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError

def generate_audio_preview(text: str, output_path: str, voice_id: str = "Joanna"):
    """
    Generates an audio file from text using Amazon Polly.

    Args:
        text: The text to convert to speech.
        output_path: The path to save the output MP3 file.
        voice_id: The Amazon Polly voice ID to use.
    """
    # AWS credentials should be configured via environment variables or IAM roles.
    # AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
    
    try:
        # Provider-specific client class
        polly_client = boto3.client("polly")

        response = polly_client.synthesize_speech(
            VoiceId=voice_id,
            OutputFormat="mp3",
            Text=text,
            Engine='neural'
        )

        with open(output_path, "wb") as f:
            f.write(response["AudioStream"].read())
        
        print(f"Audio preview saved to {output_path}")

    except (BotoCoreError, ClientError) as error:
        print(f"Error using Amazon Polly: {error}")
        raise
