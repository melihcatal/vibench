import boto3
import time

def poll_transcription_job(job_name):
    transcribe = boto3.client('transcribe')
    while True:
        response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        job_status = response['TranscriptionJob']['TranscriptionJobStatus']
        if job_status in ['COMPLETED', 'FAILED']:
            break
        print('Polling in progress...')
        time.sleep(15)
    if job_status == 'COMPLETED':
        transcript_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
        return transcript_uri
    else:
        return 'Transcription job failed'

if __name__ == '__main__':\n    job_name = 'your_transcription_job_name'
    transcript_uri = poll_transcription_job(job_name)
    print(transcript_uri)