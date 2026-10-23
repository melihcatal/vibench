import boto3

def poll_transcription_job(job_name):
    transcribe = boto3.client('transcribe', region_name='us-west-2')
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
    if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
        response = boto3.client('s3').get_object(Bucket=transcript_uri.split('/')[2], Key=transcript_uri.split('/')[3])
        transcript = response['Body'].read().decode('utf-8')
        return transcript
    else:
        return 'Transcription job failed'

if __name__ == '__main__':
    job_name = 'your_transcription_job_name'
    print(poll_transcription_job(job_name))