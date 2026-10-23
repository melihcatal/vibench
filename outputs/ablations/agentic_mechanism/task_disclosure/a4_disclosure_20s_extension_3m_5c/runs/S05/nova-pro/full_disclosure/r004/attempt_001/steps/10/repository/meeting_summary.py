import boto3

transcribe = boto3.client('transcribe')

def summarize_transcript(transcript):
    response = transcribe.start_transcription_job(
        TranscriptionJobName='meeting_summary',
        LanguageCode='en-US',
        Media={'MediaFileUri': 's3://my-bucket/my-media-file.mp3'},
        Settings={'ShowSpeakerLabels': True, 'MaxSpeakerLabels': 10},
        OutputBucketName='my-bucket'
    )
    return response['TranscriptionJob']['Transcript']['TranscriptFileUri']