import boto3

def submit_transcription(audio_file_uri):
    transcribe = boto3.client('transcribe', region_name='us-west-2')
    job_name = 'batch_transcription_job'
    job_uri = audio_file_uri

    response = transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='mp3',
        LanguageCode='en-US'
    )

    print(response)

# Example usage:
# submit_transcription('s3://your-bucket/your-audio-file.mp3')