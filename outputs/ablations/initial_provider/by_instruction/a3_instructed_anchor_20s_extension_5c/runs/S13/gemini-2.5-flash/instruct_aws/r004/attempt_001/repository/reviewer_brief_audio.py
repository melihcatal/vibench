import boto3
import os
from typing import Dict, Any

def generate_reviewer_brief_audio_aws(brief_text: str, output_format: str = 'mp3', voice_id: str = 'Joanna') -> Dict[str, Any]:
    """
    Generates spoken briefs for moderation reviewers using AWS Polly.
    """
    polly = boto3.client(
        'polly',
        region_name=os.environ.get('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

    response = polly.synthesize_speech(
        Text=brief_text,
        OutputFormat=output_format,
        VoiceId=voice_id
    )

    # The audio stream is in response['AudioStream'].read()
    # In a real application, you'd save this to a file or stream it.
    audio_stream_bytes = response['AudioStream'].read()

    return {
        'audio_content_bytes': audio_stream_bytes,
        'output_format': output_format,
        'voice_id': voice_id,
        'provider': 'AWS Polly'
    }
