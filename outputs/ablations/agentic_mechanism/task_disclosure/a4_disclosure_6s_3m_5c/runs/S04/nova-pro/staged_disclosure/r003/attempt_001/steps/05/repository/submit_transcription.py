import boto3

transcribe = boto3.client('transcribe')

def submit_transcription_job(job_name, media_uri):
    response = transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': media_uri},
        MediaFormat='mp3',
        LanguageCode='en-US'
    )
    print(response)

if __name__ == '__main__':
    job_name = 'example_job'
    media_uri = 's3://your-bucket/your-audio-file.mp3'
    submit_transcription_job(job_name, media_uri)