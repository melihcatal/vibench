import boto3

def diarized_transcript(audio_file_uri, output_bucket_uri):
    client = boto3.client('transcribe')
    response = client.start_transcription_job(
        TranscriptionJobName='diarized-transcription',
        LanguageCode='en-US',
        Media={'MediaFileUri': audio_file_uri},
        OutputBucketName=output_bucket_uri,
        MediaFormat='mp3',
        Settings={'ShowSpeakerLabels': True, 'MaxSpeakerLabels': 10}
    )
    return response