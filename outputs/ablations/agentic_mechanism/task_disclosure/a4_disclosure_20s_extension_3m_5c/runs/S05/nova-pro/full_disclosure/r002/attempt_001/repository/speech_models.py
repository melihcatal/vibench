import boto3

transcribe = boto3.client('transcribe')

def create_transcription_job(job_name, media_file_uri, language_code='en-US'):
    response = transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': media_file_uri},
        MediaFormat='mp4',
        LanguageCode=language_code,
        OutputBucketName='transcribe-output-bucket'
    )
    return response

def get_transcription_job(job_name):
    response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    return response

def normalize_transcription(transcription):
    normalized_transcription = transcription.replace('\n', ' ')
    return normalized_transcription