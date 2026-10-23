import boto3

def poll_transcription_job(job_name):
    transcribe = boto3.client('transcribe')
    while True:
        response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        job_status = response['TranscriptionJob']['TranscriptionJobStatus']
        if job_status in ['COMPLETED', 'FAILED']:
            break
    return response

def get_transcript(job_name):
    response = poll_transcription_job(job_name)
    if response['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        transcript_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
        return transcript_uri
    else:
        return 'Transcription job failed'

if __name__ == '__main__':\n    job_name = 'your_transcription_job_name'
    transcript_uri = get_transcript(job_name)
    print(transcript_uri)