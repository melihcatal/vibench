import boto3
from botocore.exceptions import BotoCoreError, ClientError


def generate_audio_preview(text: str, output_file: str):
    """
    Generates a spoken preview of translated copy using Amazon Polly.
    Saves the audio to the specified output file.
    """
    try:
        # AWS credentials are expected to be configured via environment variables
        # (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION) or an IAM role.
        polly_client = boto3.client("polly")

        response = polly_client.synthesize_speech(
            VoiceId="Joanna", OutputFormat="mp3", Text=text, Engine="neural"
        )

        with open(output_file, "wb") as f:
            f.write(response["AudioStream"].read())

        return f"Audio content written to {output_file}"

    except (BotoCoreError, ClientError) as error:
        return f"Error generating audio: {error}"
