import boto3

transcribe = boto3.client('transcribe')

def create_transcription_job(job_name, media_uri):
    response = transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': media_uri},
        MediaFormat='mp3',
        LanguageCode='en-US'
    )
    return response

def get_transcription_job(job_name):
    response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    return response

def normalize_transcription(transcription):
    normalized_transcription = transcription.lower()
    return normalized_transcription