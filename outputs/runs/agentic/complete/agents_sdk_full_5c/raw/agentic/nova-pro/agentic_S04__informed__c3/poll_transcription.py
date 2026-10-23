import boto3

transcribe_client = boto3.client('transcribe')

def poll_transcription(job_name):
    while True:
        status = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            return status
        print('Waiting for transcription job to complete...')
        time.sleep(15)