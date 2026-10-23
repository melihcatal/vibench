import os
from boto3 import client as boto3_client
from safety_client import load_aws_polly_client
from safety_models import AudioBriefRequest
from io import BytesIO

def generate_reviewer_brief_audio(brief_request: AudioBriefRequest) -> bytes:
    polly_client = load_aws_polly_client()

    response = polly_client.synthesize_speech(
        Text=brief_request.text,
        OutputFormat=brief_request.output_format,
        VoiceId=brief_request.voice_id,
        Engine='neural' # Use 'neural' for higher quality voices where available
    )

    audio_stream = response['AudioStream']
    audio_data = BytesIO()
    with audio_stream as stream:
        audio_data.write(stream.read())

    return audio_data.getvalue()
