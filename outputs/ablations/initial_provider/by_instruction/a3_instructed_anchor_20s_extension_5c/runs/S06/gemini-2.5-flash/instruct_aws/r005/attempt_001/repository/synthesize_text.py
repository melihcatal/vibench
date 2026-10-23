import boto3
import os

def synthesize_text(text: str, voice_id: str = "Joanna", output_format: str = "mp3") -> bytes:
    """
    Synthesizes plain text to an audio byte stream using AWS Polly.

    Args:
        text: The plain text to synthesize.
        voice_id: The ID of the voice to use (e.g., "Joanna", "Matthew").
        output_format: The format of the audio file (e.g., "mp3", "ogg_vorbis", "pcm").

    Returns:
        The audio as a bytes object.
    """
    polly_client = boto3.client(
        'polly',
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )

    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat=output_format,
        VoiceId=voice_id
    )

    return response['AudioStream'].read()
