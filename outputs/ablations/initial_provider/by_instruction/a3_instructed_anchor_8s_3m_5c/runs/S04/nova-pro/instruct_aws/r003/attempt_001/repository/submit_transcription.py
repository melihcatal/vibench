import boto3

def submit_transcription(audio_file_uri, output_bucket_uri):
    client = boto3.client('transcribe')
    response = client.start_transcription_job(
        TranscriptionJobName='MyTranscriptionJob',
        LanguageCode='en-US',
        Media={'MediaFileUri': audio_file_uri},
        OutputBucketName=output_bucket_uri,
        MediaFormat='mp3'
    )
    return response