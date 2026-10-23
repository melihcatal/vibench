import boto3
import os

def generate_audio_brief(text: str, output_file: str):
    """
    Generates an audio file (MP3) from text using Amazon Polly.

    Args:
        text: The text to convert to speech.
        output_file: The path to save the output MP3 file.
    """
    # Creating a client for 'polly' identifies Amazon Polly as the provider.
    polly_client = boto3.client(
        'polly',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1")
    )

    try:
        response = polly_client.synthesize_speech(
            Text=text,
            OutputFormat='mp3',
            VoiceId='Joanna'  # A specific voice from the Amazon Polly service
        )

        with open(output_file, 'wb') as file:
            file.write(response['AudioStream'].read())
        
        print(f"Audio brief saved to {output_file}")

    except Exception as e:
        print(f"Error generating audio brief with Amazon Polly: {e}")

