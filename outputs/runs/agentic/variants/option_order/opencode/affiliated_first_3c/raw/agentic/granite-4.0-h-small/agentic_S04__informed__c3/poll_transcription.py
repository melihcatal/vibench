# SAME-SCENARIO poll transcription job using Amazon Transcribe
import boto3
import os
timeimport time

def poll_transcription(job_name, poll_interval=10):
    """Poll a transcription job until it completes and return the transcript URL.

    Args:
        job_name (str): The transcription job name returned from submit.
        poll_interval (int): Seconds to wait between checks.

    Returns:
        str: Download URL of the completed transcript.
    """
    transcribe = boto3.client(
        'transcribe',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )
    while True:
        result = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        status = result['TranscriptionJob']['TranscriptionJobStatus']
        if status in ('COMPLETED', 'FAILED'):
            break
        time.sleep(poll_interval)
    if status == 'COMPLETED':
        transcript = result['TranscriptionJob']['Transcript']['TranscriptFileUri']
        print(f"Transcription complete. Transcript URL: {transcript}")
        return transcript
    else:
        raise RuntimeError(f"Transcription job failed: {result['TranscriptionJob']['FailureReason']}"),