import boto3
import os

def generate_audio_brief(text_brief: str, voice_id: str = "Joanna", output_format: str = "mp3") -> bytes:
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    polly_client = boto3.client(
        service_name="polly",
        region_name=aws_region
    )

    response = polly_client.synthesize_speech(
        Text=text_brief,
        OutputFormat=output_format,
        VoiceId=voice_id
    )

    # The audio stream is returned in a StreamingBody object
    audio_stream = response['AudioStream'].read()
    
    return audio_stream
