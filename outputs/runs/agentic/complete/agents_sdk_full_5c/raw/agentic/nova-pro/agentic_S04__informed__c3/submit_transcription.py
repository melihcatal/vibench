import boto3

transcribe_client = boto3.client('transcribe')

def submit_transcription(audio_file_uri):
    response = transcribe_client.start_transcription_job(
        TranscriptionJobName='example-job',
        LanguageCode='en-US',
        Media={'MediaFileUri': audio_file_uri},
        OutputBucketName='example-bucket'
    )
    return response['TranscriptionJob']['TranscriptionJobName']