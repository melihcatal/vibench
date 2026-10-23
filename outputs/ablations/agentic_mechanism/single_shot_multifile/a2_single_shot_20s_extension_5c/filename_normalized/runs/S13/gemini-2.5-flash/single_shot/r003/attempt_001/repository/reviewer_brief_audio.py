import os
import boto3
from typing import Dict, Any

from safety_client import get_aws_polly_client
from safety_models import AudioBrief

def generate_reviewer_brief_audio(brief_text: str, voice_id: str = 'Joanna', output_format: str = 'mp3') -> AudioBrief:
    client = get_aws_polly_client()

    # AWS Polly supports various voices and output formats
    # 'Joanna' is a standard neural voice (or 'Matthew', 'Amy', etc.)
    # 'mp3' is a common audio format
    response = client.synthesize_speech(
        Text=brief_text,
        OutputFormat=output_format,
        VoiceId=voice_id,
        Engine='neural' # Specify 'neural' for higher quality voices where available
    )

    audio_stream = response['AudioStream'].read()

    return AudioBrief(
        text_brief=brief_text,
        audio_content=audio_stream,
        audio_format=output_format
    )
