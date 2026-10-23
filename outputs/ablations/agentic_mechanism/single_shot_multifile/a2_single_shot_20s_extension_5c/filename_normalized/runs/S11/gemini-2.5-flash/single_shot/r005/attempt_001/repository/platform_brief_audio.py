import os
import boto3
from botocore.exceptions import ClientError
from typing import Dict, Any

def generate_brief_audio(text_content: str, voice_id: str = "Joanna") -> Dict[str, Any]:
    """Generate spoken briefings from platform outputs using AWS Polly."""
    region_name = os.getenv("AWS_REGION", "us-east-1")
    
    try:
        polly_client = boto3.client("polly", region_name=region_name)

        response = polly_client.synthesize_speech(
            Text=text_content,
            OutputFormat="mp3",
            VoiceId=voice_id
        )

        # Access the audio stream from the response
        if "AudioStream" in response:
            audio_stream = response["AudioStream"].read()
            return {
                "audio_content": audio_stream,
                "output_format": "mp3",
                "voice_id": voice_id
            }
        else:
            raise RuntimeError("No AudioStream found in AWS Polly response.")

    except ClientError as e:
        raise RuntimeError(f"AWS Polly synthesize speech failed: {e}")
