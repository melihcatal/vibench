import boto3

transcribe = boto3.client('transcribe')

def diarized_transcript(file_uri, job_name):
    response = transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': file_uri},
        MediaFormat='mp3',
        LanguageCode='en-US',
        Settings={'ShowSpeakerLabels': True, 'MaxSpeakerLabels': 10}
    )
    return response