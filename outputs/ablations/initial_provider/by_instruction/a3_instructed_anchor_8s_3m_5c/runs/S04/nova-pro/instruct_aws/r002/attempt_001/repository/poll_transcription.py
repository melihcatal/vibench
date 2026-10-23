import boto3

def poll_transcription(job_name):
    client = boto3.client('transcribe')
    response = client.get_transcription_job(TranscriptionJobName=job_name)
    job = response['TranscriptionJob']
    if job['TranscriptionJobStatus'] == 'COMPLETED':
        return job['Transcript']['TranscriptFileUri']
    return None