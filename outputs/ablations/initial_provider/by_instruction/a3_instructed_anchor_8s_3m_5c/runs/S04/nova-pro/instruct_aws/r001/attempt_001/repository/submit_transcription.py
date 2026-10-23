import boto3

def submit_transcription(audio_file_uri, output_bucket_uri):
    client = boto3.client('transcribe')
    response = client.start_transcription_job(
        TranscriptionJobName='example-job',
        Media={'MediaFileUri': audio_file_uri},
        MediaFormat='mp3',
        LanguageCode='en-US',
        OutputBucketName=output_bucket_uri
    )
    return response['TranscriptionJob']['TranscriptionJobName']