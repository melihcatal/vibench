import boto3

def poll_transcription_job(job_name):
    transcribe_client = boto3.client('transcribe')
    while True:
        response = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        job_status = response['TranscriptionJob']['TranscriptionJobStatus']
        if job_status in ['COMPLETED', 'FAILED']:
            break
    if job_status == 'COMPLETED':
        transcript_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
        return transcript_uri
    else:
        return 'Transcription job failed.'

# Example usage
transcript_uri = poll_transcription_job('your_job_name')
print(transcript_uri)