import boto3
from botocore.exceptions import ClientError

def generate_spoken_brief(text: str, output_format: str = "mp3", voice_id: str = "Joanna") -> bytes:
    """
    Generates a spoken brief from the model output using AWS Polly.
    """
    polly = boto3.client(
        service_name="polly",
        region_name="us-east-1"
    )

    try:
        response = polly.synthesize_speech(
            Text=text,
            OutputFormat=output_format,
            VoiceId=voice_id
        )
        return response['AudioStream'].read()
    except ClientError as e:
        print(f"Error synthesizing speech: {e}")
        return b""

