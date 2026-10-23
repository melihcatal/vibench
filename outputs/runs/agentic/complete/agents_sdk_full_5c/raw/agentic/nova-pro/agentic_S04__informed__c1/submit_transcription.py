import boto3

transcribe = boto3.client('transcribe')

def submit_transcription(audio_file):
    job_name = 'my-transcription-job'
    job_uri = 's3://my-bucket/' + audio_file
    response = transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='mp3',
        LanguageCode='en-US'
    )
    return response