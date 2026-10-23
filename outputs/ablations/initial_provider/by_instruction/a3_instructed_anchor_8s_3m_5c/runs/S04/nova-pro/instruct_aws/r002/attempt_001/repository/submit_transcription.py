import boto3

def submit_transcription(file_uri, job_name, language_code):
    client = boto3.client('transcribe')
    response = client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': file_uri},
        LanguageCode=language_code,
        OutputBucketName='your-output-bucket'
    )
    return response