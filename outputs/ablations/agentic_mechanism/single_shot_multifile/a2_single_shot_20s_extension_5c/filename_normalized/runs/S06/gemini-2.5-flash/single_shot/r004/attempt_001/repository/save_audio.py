import os
import boto3
from speech_client import get_aws_s3_client
from speech_models import AudioSaveRequest, AudioSaveResult

def save_audio_to_s3(request: AudioSaveRequest) -> AudioSaveResult:
    s3_client = get_aws_s3_client()
    
    bucket_name = os.getenv("AWS_S3_BUCKET_NAME")
    if not bucket_name:
        raise ValueError("AWS_S3_BUCKET_NAME environment variable must be set.")

    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=request.filename,
            Body=request.audio_content,
            ContentType=request.content_type
        )
        object_url = f"https://{bucket_name}.s3.amazonaws.com/{request.filename}"
        
        return AudioSaveResult(
            url=object_url,
            size_bytes=len(request.audio_content)
        )
    except Exception as e:
        raise RuntimeError(f"Failed to save audio to S3: {e}")
