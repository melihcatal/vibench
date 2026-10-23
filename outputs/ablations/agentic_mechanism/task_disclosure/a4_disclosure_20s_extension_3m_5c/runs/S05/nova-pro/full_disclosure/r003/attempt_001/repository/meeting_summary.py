import boto3

transcribe = boto3.client('transcribe')

def summarize_transcript(transcript):
    response = transcribe.start_transcription_job(
        TranscriptionJobName='meeting-summary',
        LanguageCode='en-US',
        Media={'MediaFileUri': 's3://your-bucket/your-file.mp3'},
        Settings={'ShowSpeakerLabels': True, 'MaxSpeakerLabels': 10},
        OutputBucketName='your-output-bucket'
    )
    return response
