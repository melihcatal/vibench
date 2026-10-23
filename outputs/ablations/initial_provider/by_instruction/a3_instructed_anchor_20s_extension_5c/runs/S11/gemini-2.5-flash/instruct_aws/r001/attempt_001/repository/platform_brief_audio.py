import boto3
from model_client import get_polly_client

def generate_audio_from_text(
    text: str,
    output_format: str = "mp3",
    voice_id: str = "Joanna",
) -> bytes:
    """
    Generates spoken briefings from platform outputs using AWS Polly.
    Returns the audio stream as bytes.
    """
    client = get_polly_client()

    response = client.synthesize_speech(
        Text=text,
        OutputFormat=output_format,
        VoiceId=voice_id
    )

    return response["AudioStream"].read()
