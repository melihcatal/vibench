from typing import Dict, Any
import boto3
import os

def generate_platform_brief_audio(text: str, output_format: str = "mp3") -> Dict[str, Any]:
    client = boto3.client(
        "polly",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )
    
    response = client.synthesize_speech(
        Text=text,
        OutputFormat=output_format,
        VoiceId="Joanna",
        Engine="neural",
    )
    
    return {
        "audio_stream": response["AudioStream"].read(),
        "content_type": response["ContentType"],
        "voice": "Joanna",
        "engine": "neural",
    }