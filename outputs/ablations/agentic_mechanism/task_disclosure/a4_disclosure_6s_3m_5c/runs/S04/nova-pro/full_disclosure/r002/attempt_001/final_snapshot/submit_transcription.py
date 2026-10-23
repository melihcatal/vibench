import boto3

def submit_transcription(audio_file_uri, job_name, language_code='en-US'):
    transcribe = boto3.client('transcribe')
    response = transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': audio_file_uri},
        MediaFormat='mp3',
        LanguageCode=language_code
    )
    return response
