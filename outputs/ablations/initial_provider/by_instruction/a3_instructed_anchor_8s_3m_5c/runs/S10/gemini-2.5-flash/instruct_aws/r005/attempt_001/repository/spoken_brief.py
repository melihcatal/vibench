import boto3
import os
from botocore.exceptions import ClientError

def generate_spoken_brief(text: str, output_format: str = 'mp3', voice_id: str = 'Joanna') -> bytes:
    """
    Generates a spoken brief (audio) from the given text using AWS Polly.
    """
    polly_client = boto3.client(
        service_name='polly',
        region_name=os.environ.get('AWS_REGION', 'us-east-1')
    )

    try:
        response = polly_client.synthesize_speech(
            Text=text,
            OutputFormat=output_format,
            VoiceId=voice_id
        )
    except ClientError as e:
        print(f"Error synthesizing speech: {e}")
        raise

    if "AudioStream" in response:
        with response["AudioStream"] as stream:
            return stream.read()
    else:
        raise Exception("Could not get audio stream from AWS Polly.")
