import boto3

transcribe_client = boto3.client('transcribe')

def timestamped_transcript(job_name):
    response = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
    job = response['TranscriptionJob']
    if job['TranscriptionJobStatus'] == 'COMPLETED':
        transcript_uri = job['Transcript']['TranscriptFileUri']
        transcript_response = transcribe_client.get_object(Bucket='example-bucket', Key=transcript_uri.split('/')[-1])
        transcript_content = transcript_response['Body'].read().decode('utf-8')
        return transcript_content
    return None