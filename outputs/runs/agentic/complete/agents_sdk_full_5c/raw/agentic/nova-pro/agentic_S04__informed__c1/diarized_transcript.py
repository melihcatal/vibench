import boto3

transcribe = boto3.client('transcribe')

def diarized_transcript(job_name):
    response = transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': 's3://my-bucket/my-audio-file.mp3'},
        MediaFormat='mp3',
        LanguageCode='en-US',
        Settings={'ShowSpeakerLabels': True, 'MaxSpeakerLabels': 10}
    )
    return response