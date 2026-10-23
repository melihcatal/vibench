import boto3
import os
from typing import Optional

def localized_audio_preview(text: str, output_file: str = "preview.mp3", voice_id: str = "Joanna", language_code: str = "en-US") -> str:
    """
    Generate spoken previews of translated copy using Amazon Polly.
    """
    polly = boto3.client(
        "polly",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name="us-east-1"
    )
    
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat="mp3",
        VoiceId=voice_id,
        LanguageCode=language_code
    )
    
    with open(output_file, "wb") as f:
        f.write(response["AudioStream"].read())
    
    return output_file