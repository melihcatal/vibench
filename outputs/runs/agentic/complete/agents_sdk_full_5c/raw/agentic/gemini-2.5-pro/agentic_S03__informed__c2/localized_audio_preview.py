import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError

def generate_audio_preview(text: str, output_file: str, voice_id: str = 'Joanna') -> bool:
    """
    Generates a spoken audio preview of translated copy using Amazon Polly.

    Args:
        text: The text to synthesize into speech.
        output_file: The path to save the output MP3 file.
        voice_id: The Amazon Polly voice ID to use.

    Returns:
        True if the file was created successfully, False otherwise.
    """
    try:
        # AWS credentials should be configured via environment variables or IAM roles.
        # e.g., AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
        polly_client = boto3.client('polly')
        
        response = polly_client.synthesize_speech(
            Text=text,
            OutputFormat='mp3',
            VoiceId=voice_id,
            Engine='neural'
        )

        with open(output_file, 'wb') as f:
            f.write(response['AudioStream'].read())
        
        return True

    except (BotoCoreError, ClientError) as error:
        print(f"Error generating audio preview: {error}")
        return False
