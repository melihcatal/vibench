import boto3

transcribe = boto3.client('transcribe')

def timestamped_transcript(job_name):
    response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    if response['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        transcript_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
        transcript = boto3.client('s3').get_object(Bucket='transcribe-bucket', Key=transcript_uri.split('/')[-1])['Body'].read().decode('utf-8')
        return transcript
    else:
        raise Exception('Transcription not completed.')