import boto3

transcribe = boto3.client('transcribe')

def submit_transcription(file_uri, job_name):
    response = transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': file_uri},
        MediaFormat='mp3',
        LanguageCode='en-US'
    )
    return response