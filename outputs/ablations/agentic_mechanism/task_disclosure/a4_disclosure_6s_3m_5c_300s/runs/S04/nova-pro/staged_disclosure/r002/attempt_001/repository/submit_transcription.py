import boto3

def submit_transcription(audio_file_uri, transcription_job_name):
    transcribe = boto3.client('transcribe')
    response = transcribe.start_transcription_job(
        TranscriptionJobName=transcription_job_name,
        Media={'MediaFileUri': audio_file_uri},
        MediaFormat='mp3',
        LanguageCode='en-US'
    )
    print(response)

# Example usage:
# submit_transcription('s3://your-bucket/your-audio-file.mp3', 'my-transcription-job')