import boto3
import os
from contextlib import closing

def generate_reviewer_brief_audio(brief_text: str, output_filepath: str = "reviewer_brief.mp3"):
    """
    Generates an audio brief for moderation reviewers using AWS Polly.
    Saves the audio to a specified MP3 file.
    """
    polly_client = boto3.client(
        'polly',
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )

    response = polly_client.synthesize_speech(
        Text=brief_text,
        OutputFormat='mp3',
        VoiceId='Joanna'  # You can choose other voices like 'Matthew', 'Amy', etc.
    )

    if "AudioStream" in response:
        with closing(response['AudioStream']) as stream:
            with open(output_filepath, "wb") as file:
                file.write(stream.read())
        print(f"Audio brief saved to {output_filepath}")
    else:
        print("Could not retrieve audio stream.")
