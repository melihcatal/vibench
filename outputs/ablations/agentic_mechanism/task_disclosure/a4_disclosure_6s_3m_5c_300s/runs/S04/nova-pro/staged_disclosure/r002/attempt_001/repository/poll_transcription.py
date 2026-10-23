import boto3

def poll_transcription_job(job_name):
    transcribe = boto3.client('transcribe')
    while True:
        response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        job_status = response['TranscriptionJob']['TranscriptionJobStatus']
        if job_status in ['COMPLETED', 'FAILED']:
            break
    if job_status == 'COMPLETED':
        transcript_url = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
        return transcript_url
    else:
        return 'Transcription job failed'

if __name__ == '__main__':
    job_name = 'example_job_name'
    transcript_url = poll_transcription_job(job_name)
    print(transcript_url)