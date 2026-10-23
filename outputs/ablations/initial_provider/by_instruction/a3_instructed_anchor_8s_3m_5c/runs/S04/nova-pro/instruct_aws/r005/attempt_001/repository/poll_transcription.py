import boto3

def poll_transcription(job_name):
    client = boto3.client('transcribe')
    
    while True:
        status = client.get_transcription_job(TranscriptionJobName=job_name)
        job_status = status['TranscriptionJob']['TranscriptionJobStatus']
        
        if job_status in ['COMPLETED', 'FAILED']:
            break
        print('Polling...')
        time.sleep(15)
    
    if job_status == 'COMPLETED':
        transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
        return transcript_uri
    else:
        return 'Transcription failed'