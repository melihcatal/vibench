# Generate a spoken brief from model output using Amazon Polly via Boto3
to_boto3 = __import__("boto3")
import json


def create_spoken_brief(
    text: str, voice_id: str = "Joanna", output_format: str = "mp3"
) -> bytes:
    """Synthesize speech from text using Amazon Polly.

    Args:
        text: Text to convert to speech.
        voice_id: Polly voice identifier.
        output_format: Audio format (e.g., mp3, ogg_vorbis).

    Returns:
        Binary audio data.
    """
    client = to_boto3.client(
        service_name="polly",
        region_name="us-east-1",
        aws_access_key_id="AWS_ACCESS_KEY_ID",
        aws_secret_access_key="AWS_SECRET_ACCESS_KEY",
    )
    response = client.synthesize_speech(
        Text=text,
        OutputFormat=output_format,
        VoiceId=voice_id,
    )
    return response["AudioStream"].read()
