import boto3
import os

def generate_polly_audio(text: str, voice_id: str = "Joanna", output_format: str = "mp3") -> bytes:
    """
    Generates spoken briefings from platform outputs using AWS Polly.

    Args:
        text (str): The text to synthesize into speech.
        voice_id (str): The ID of the voice to use (e.g., "Joanna", "Matthew").
        output_format (str): The format of the output audio (e.g., "mp3", "pcm", "ogg_vorbis").

    Returns:
        bytes: The audio stream of the synthesized speech.
    """
    client = boto3.client(
        "polly",
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    response = client.synthesize_speech(
        Text=text,
        OutputFormat=output_format,
        VoiceId=voice_id
    )

    if "AudioStream" in response:
        with response["AudioStream"] as stream:
            return stream.read()
    else:
        raise Exception("Could not get audio stream from AWS Polly.")
