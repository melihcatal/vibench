import boto3


def tts_qa_transcript(audio_file_path):
    client = boto3.client('transcribe')
    job_name = 'tts_qa_transcript_job'
    job_uri = 's3://your-bucket/' + audio_file_path
    client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='mp3',
        LanguageCode='en-US'
    )
    while True:
        status = client.get_transcription_job(TranscriptionJobName=job_name)['TranscriptionJob']['TranscriptionJobStatus']
        if status in ['COMPLETED', 'FAILED']:
            break
    if status == 'COMPLETED':
        transcript_uri = client.get_transcription_job(TranscriptionJobName=job_name)['TranscriptionJob']['Transcript']['TranscriptFileUri']
        response = boto3.client('s3').get_object(Bucket='your-bucket', Key=transcript_uri.split('/')[-1])
        return response['Body'].read().decode('utf-8')
    else:
        return 'Transcription job failed.'