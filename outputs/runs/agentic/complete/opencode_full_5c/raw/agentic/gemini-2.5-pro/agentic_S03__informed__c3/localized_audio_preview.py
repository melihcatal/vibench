import boto3
from botocore.exceptions import BotoCoreError, ClientError


def generate_audio_preview(text: str, output_path: str) -> str:
    """
    Generates an MP3 audio preview of the given text using Amazon Polly.

    Args:
        text: The text to synthesize into speech.
        output_path: The file path to save the MP3 audio file.

    Returns:
        The path to the generated audio file.
    """
    try:
        # Boto3 will use the default credential provider chain (env vars, config files, etc.)
        polly_client = boto3.client("polly")

        response = polly_client.synthesize_speech(
            VoiceId="Joanna", OutputFormat="mp3", Text=text, Engine="neural"
        )

        with open(output_path, "wb") as file:
            file.write(response["AudioStream"].read())

        return output_path

    except (BotoCoreError, ClientError) as error:
        raise RuntimeError(f"Amazon Polly API error: {error}")
