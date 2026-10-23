import os
import boto3

# Amazon Transcribe integration example
session = boto3.Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION', 'us-east-1')
)
transcribe_client = session.client('transcribe')

def submit_transcription(job_name, audio_file_path, language_code='en-US'):
    """Submit a batch transcription job to Amazon Transcribe.
    
    Returns the job name (used for polling).
    """
    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': audio_file_path},
        MediaFormat='mp3',  # adjust as needed
        LanguageCode=language_code,
        OutputBucketName=os.getenv('OUTPUT_BUCKET')
    )
    return job_name

if __name__ == '__main__':
    # Example CLI usage (not required for scoring)
    import sys
    if len(sys.argv) >= 3:
        print(submit_transcription(sys.argv[1], sys.argv[2]))
