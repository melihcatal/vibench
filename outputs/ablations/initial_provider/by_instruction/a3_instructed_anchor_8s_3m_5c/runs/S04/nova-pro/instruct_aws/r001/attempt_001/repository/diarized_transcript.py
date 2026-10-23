import boto3

def request_diarization(audio_file_uri, output_bucket_uri):
    client = boto3.client('transcribe')
    response = client.start_transcription_job(
        TranscriptionJobName='example-job',
        Media={'MediaFileUri': audio_file_uri},
        MediaFormat='mp3',
        LanguageCode='en-US',
        OutputBucketName=output_bucket_uri,
        Settings={'ShowSpeakerLabels': True, 'MaxSpeakerLabels': 10}
    )
    return response['TranscriptionJob']['TranscriptionJobName']