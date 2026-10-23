import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError

def generate_reviewer_brief_audio(brief_text: str, output_path: str) -> bool:
    """
    Generates an audio file from text using Amazon Polly for a reviewer brief.

    Args:
        brief_text: The text to convert to speech.
        output_path: The local file path to save the MP3 audio file.

    Returns:
        True if the file was successfully created, False otherwise.
    """
    try:
        # AWS credentials should be configured in the environment (e.g., via env vars)
        # AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
        polly_client = boto3.client('polly')
    except (BotoCoreError, ClientError) as e:
        print(f"Error creating Boto3 Polly client: {e}")
        return False
        
    if not brief_text:
        print("Input text is empty, cannot generate audio.")
        return False

    try:
        response = polly_client.synthesize_speech(
            Text=brief_text,
            OutputFormat='mp3',
            VoiceId='Joanna',  # A standard, clear voice
            Engine='neural'
        )
    except (BotoCoreError, ClientError) as error:
        print(f"Error calling Amazon Polly API: {error}")
        return False

    # The audio is returned as a stream in the response.
    if "AudioStream" in response:
        try:
            with open(output_path, 'wb') as file:
                file.write(response['AudioStream'].read())
            print(f"Audio brief saved to {output_path}")
            return True
        except IOError as e:
            print(f"Error writing audio file to {output_path}: {e}")
            return False
    else:
        print("Could not find audio stream in Polly response.")
        return False
