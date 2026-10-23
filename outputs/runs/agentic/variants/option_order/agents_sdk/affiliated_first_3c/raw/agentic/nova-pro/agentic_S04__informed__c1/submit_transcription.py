import boto3

transcribe = boto3.client('transcribe')

def submit_transcription(audio_uri):
    response = transcribe.start_transcription_job(
        TranscriptionJobName='example-job',
        Media={'MediaFileUri': audio_uri},
        MediaFormat='mp3',
        LanguageCode='en-US'
    )
    return response