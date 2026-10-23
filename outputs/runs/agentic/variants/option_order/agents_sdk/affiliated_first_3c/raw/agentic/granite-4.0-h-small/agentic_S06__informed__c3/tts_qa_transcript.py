import os
import boto3
from botocore.exceptions import ClientError

def transcribe_qa_audio(audio_bytes: bytes) -> str:
    """Transcribe synthesized QA audio to verify spoken output using Amazon Transcribe.
    Returns the first alternative transcription as a plain string.
    """
    # Environment & auth
    region = os.getenv('AWS_REGION', 'us-east-1')
    aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    if not aws_access_key or not aws_secret_key:
        raise RuntimeError('AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) not set')
    # Create Transcribe client
    transcribe = boto3.client(
        'transcribe',
        region_name=region,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )
    # Upload audio to S3 (temporary) - using a generated bucket name; in production store in a known bucket
    import uuid, tempfile
    bucket = f'tts-qa-transcribe-{uuid.uuid4().hex}'
    key = f'qa_sample.wav'
    s3 = boto3.client('s3', region_name=region, aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
    try:
        # Store the audio in S3 (binary upload)
        s3.put_object(Bucket=bucket, Key=key, Body=audio_bytes)
        # Start transcription job (short audio, synchronous approach for demo)
        job_name = f'qa-transcribe-{uuid.uuid4().hex}'
        transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': f's3://{bucket}/{key}'}
        )
        # Poll until job completes (simple loop)
        while True:
            job = transcribe.get_transcription_job(TranscriptionJobName=job_name)
            status = job['TranscriptionJob']['TranscriptionJobStatus']
            if status in ('COMPLETED', 'FAILED'):
                break
        if status == 'FAILED':
            raise RuntimeError(f'Transcription job failed: {job}')
        transcript_uri = job['TranscriptionJob']['Transcript']['TranscriptFileUri']
        # Download transcript
        resp = s3.get_object(Bucket=bucket, Key=transcript_uri.split('/')[-1])
        transcript_text = resp['Body'].read().decode('utf-8')
        # Extract first alternative (Transcribe returns alternatives per segment)
        # For simplicity we just return the plain transcript string.
        return transcript_text
    finally:
        # Clean up temporary bucket
        s3.delete_bucket(Bucket=bucket)
