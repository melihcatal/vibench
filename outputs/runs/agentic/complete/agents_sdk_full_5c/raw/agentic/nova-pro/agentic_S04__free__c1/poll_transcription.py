import boto3

transcribe = boto3.client('transcribe')

def poll_transcription(job_name):
    response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    while response['TranscriptionJob']['TranscriptionJobStatus'] in ['QUEUED', 'IN_PROGRESS']:
        print(f"Job {job_name} is {response['TranscriptionJob']['TranscriptionJobStatus']}")
        time.sleep(15)
        response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    if response['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        return response['TranscriptionJob']['Transcript']['TranscriptFileUri']
    else:
        raise Exception('Transcription failed or was stopped.')