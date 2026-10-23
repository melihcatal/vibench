import boto3
import os

def generate_audio_brief(text: str, output_format: str = "mp3", voice_id: str = "Joanna") -> bytes:
    """
    Generates a spoken brief from retrieved search results using AWS Polly.
    Returns the audio content as bytes.
    """
    polly = boto3.client(
        service_name="polly",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

    response = polly.synthesize_speech(
        Text=text,
        OutputFormat=output_format,
        VoiceId=voice_id
    )

    if "AudioStream" in response:
        with response["AudioStream"] as stream:
            return stream.read()
    else:
        raise Exception("Could not stream audio")
