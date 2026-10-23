import boto3
import os
from io import BytesIO

def generate_audio_with_amazon_polly(text: str, voice_id: str = "Joanna", output_format: str = "mp3"):
    """
    Generates spoken audio from text using Amazon Polly.
    Returns audio content as bytes.
    """
    client = boto3.client(
        "polly",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    try:
        response = client.synthesize_speech(
            Text=text,
            OutputFormat=output_format,
            VoiceId=voice_id
        )

        if "AudioStream" in response:
            with BytesIO() as audio_stream:
                audio_stream.write(response["AudioStream"].read())
                return audio_stream.getvalue()
        else:
            print("Could not find AudioStream in Polly response.")
            return None
    except Exception as e:
        print(f"Error generating speech with Amazon Polly: {e}")
        return None
