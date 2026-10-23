import boto3

transcribe_client = boto3.client('transcribe')

def request_diarization(audio_file_uri):
    response = transcribe_client.start_transcription_job(
        TranscriptionJobName='example-diarization-job',
        LanguageCode='en-US',
        Media={'MediaFileUri': audio_file_uri},
        Settings={'ShowSpeakerLabels': True, 'MaxSpeakerLabels': 10},
        OutputBucketName='example-bucket'
    )
    return response['TranscriptionJob']['TranscriptionJobName']