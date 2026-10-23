import boto3

transcribe = boto3.client('transcribe')

def poll_transcription(job_name):
    while True:
        response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        job_status = response['TranscriptionJob']['TranscriptionJobStatus']
        if job_status in ['COMPLETED', 'FAILED']:
            return response
        print('Polling...')
        time.sleep(15)