import boto3

transcribe = boto3.client('transcribe')

def submit_transcription(audio_file_uri):
    response = transcribe.start_transcription_job(
        TranscriptionJobName='example-job',
        Media={'MediaFileUri': audio_file_uri},
        MediaFormat='mp4',
        LanguageCode='en-US'
    )
    return response