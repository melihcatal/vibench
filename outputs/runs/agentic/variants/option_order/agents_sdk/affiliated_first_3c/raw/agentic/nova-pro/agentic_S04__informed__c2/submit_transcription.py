import boto3

transcribe_client = boto3.client('transcribe')

def submit_transcription(file_uri):
    response = transcribe_client.start_transcription_job(
        TranscriptionJobName='example_job',
        LanguageCode='en-US',
        Media={'MediaFileUri': file_uri},
        OutputBucketName='example-bucket'
    )
    return response