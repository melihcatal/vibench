import boto3

def request_diarization(job_name):
    client = boto3.client('transcribe')
    
    response = client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': 's3://your-bucket/your-audio-file.mp3'},
        MediaFormat='mp3',
        LanguageCode='en-US',
        Settings={'ShowSpeakerLabels': True, 'MaxSpeakerLabels': 10}
    )
    
    return response