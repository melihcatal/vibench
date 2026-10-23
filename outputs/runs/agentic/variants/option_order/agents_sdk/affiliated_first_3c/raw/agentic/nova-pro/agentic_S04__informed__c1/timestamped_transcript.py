import boto3

transcribe = boto3.client('transcribe')

def timestamped_transcript(job_name):
    response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    job = response['TranscriptionJob']
    while job['TranscriptionJobStatus'] in ['QUEUED', 'IN_PROGRESS']:
        response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        job = response['TranscriptionJob']
    if job['TranscriptionJobStatus'] == 'COMPLETED':
        transcript_uri = job['Transcript']['TranscriptFileUri']
        transcript_response = boto3.client('s3').get_object(Bucket='your-bucket-name', Key=transcript_uri.split('/')[-1])
        transcript_content = transcript_response['Body'].read().decode('utf-8')
        return transcript_content
    return None