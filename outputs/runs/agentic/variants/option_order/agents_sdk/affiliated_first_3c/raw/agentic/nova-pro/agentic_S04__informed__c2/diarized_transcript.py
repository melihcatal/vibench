import boto3

transcribe_client = boto3.client('transcribe')

def diarized_transcript(file_uri):
    response = transcribe_client.start_transcription_job(
        TranscriptionJobName='example_diarization_job',
        LanguageCode='en-US',
        Media={'MediaFileUri': file_uri},
        OutputBucketName='example-bucket',
        Settings={'ShowSpeakerLabels': True, 'MaxSpeakerLabels': 10}
    )
    return response