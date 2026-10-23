import boto3

transcribe = boto3.client('transcribe')

def poll_transcription(job_name):
    response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    job = response['TranscriptionJob']
    while job['TranscriptionJobStatus'] in ['QUEUED', 'IN_PROGRESS']:
        response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        job = response['TranscriptionJob']
    return job['Transcript'] if job['TranscriptionJobStatus'] == 'COMPLETED' else None