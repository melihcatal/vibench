import boto3

transcribe = boto3.client('transcribe')

def diarized_transcript(audio_file_uri):
    response = transcribe.start_transcription_job(
        TranscriptionJobName='example-job',
        Media={'MediaFileUri': audio_file_uri},
        MediaFormat='mp4',
        LanguageCode='en-US',
        Settings={'ShowSpeakerLabels': True, 'MaxSpeakerLabels': 10}
    )
    return response