import boto3

def poll_transcription_job(job_name):
    transcribe = boto3.client('transcribe')
    while True:
        job = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        job_status = job['TranscriptionJob']['TranscriptionJobStatus']
        if job_status in ['COMPLETED', 'FAILED']:
            break
    return job

def get_transcript(job):
    if job['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        transcript_uri = job['TranscriptionJob']['Transcript']['TranscriptFileUri']
        response = boto3.client('s3').get_object(Bucket=transcript_uri.split('/')[2], Key=transcript_uri.split('/')[3])
        transcript = response['Body'].read().decode('utf-8')
        return transcript
    else:
        return 'Transcription job failed'

if __name__ == '__main__':
    job_name = 'example_job_name'
    job = poll_transcription_job(job_name)
    transcript = get_transcript(job)
    print(transcript)