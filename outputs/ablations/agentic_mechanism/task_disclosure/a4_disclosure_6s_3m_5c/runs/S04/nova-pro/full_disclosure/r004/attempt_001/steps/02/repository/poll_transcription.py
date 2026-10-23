import boto3

def poll_transcription_job(job_name):
    transcribe_client = boto3.client('transcribe')
    while True:
        job = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        job_status = job['TranscriptionJob']['TranscriptionJobStatus']
        if job_status in ['COMPLETED', 'FAILED']:
            break
    if job_status == 'COMPLETED':
        transcript_uri = job['TranscriptionJob']['Transcript']['TranscriptFileUri']
        response = boto3.client('s3').get_object(Bucket=transcript_uri.split('/')[2], Key=transcript_uri.split('/')[3])
        transcript = response['Body'].read().decode('utf-8')
        return transcript
    else:
        return 'Transcription job failed'

# Example usage:
# transcript = poll_transcription_job('your_transcription_job_name')