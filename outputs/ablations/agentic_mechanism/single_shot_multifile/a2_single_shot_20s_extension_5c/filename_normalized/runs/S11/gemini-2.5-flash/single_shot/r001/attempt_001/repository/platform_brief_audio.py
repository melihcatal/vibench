from model_models import AudioRequest
from model_client import get_aws_polly_client
import boto3

def generate_polly_audio(request: AudioRequest) -> bytes:
    client = get_aws_polly_client()
    try:
        response = client.synthesize_speech(
            Text=request.text,
            OutputFormat=request.output_format,
            VoiceId=request.voice_id
        )
        if "AudioStream" in response:
            audio_stream = response["AudioStream"].read()
            return audio_stream
        else:
            raise RuntimeError("Could not retrieve audio stream from AWS Polly.")
    except boto3.exceptions.S3UploadFailedError as e: raise RuntimeError(f"AWS Polly S3 upload failed: {e}")
    except Exception as e: raise RuntimeError(f"AWS Polly API error: {e}")