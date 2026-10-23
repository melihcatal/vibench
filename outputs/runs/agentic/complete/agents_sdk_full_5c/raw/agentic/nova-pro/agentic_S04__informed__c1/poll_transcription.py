import boto3

transcribe = boto3.client('transcribe')

def poll_transcription(job_name):
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        job_status = status['TranscriptionJob']['TranscriptionJobStatus']
        if job_status in ['COMPLETED', 'FAILED']:
            return status
        print('Waiting for transcription...')
