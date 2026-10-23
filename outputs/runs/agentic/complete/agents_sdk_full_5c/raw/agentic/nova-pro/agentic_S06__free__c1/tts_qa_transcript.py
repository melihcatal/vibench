import boto3

def transcribe_audio(audio_data):
    transcribe_client = boto3.client('transcribe')
    job_name = 'tts_qa_transcript'
    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': 's3://your-bucket/your-audio-file.mp3'},
        MediaFormat='mp3',
        LanguageCode='en-US'
    )
    while True:
        status = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
    if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
        transcript_response = boto3.client('s3').get_object(Bucket='your-bucket', Key=transcript_uri.split('/')[-1])
        return transcript_response['Body'].read().decode('utf-8')
    else:
        return 'Transcription failed'