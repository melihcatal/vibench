import boto3


def transcribe_qa_sample(audio_bytes):
    client = boto3.client('transcribe')
    job_name = 'qa-transcription-job'
    job_uri = 's3://my-bucket/qa-audio.mp3'
    client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='mp3',
        LanguageCode='en-US'
    )
    # Wait for the job to complete and return the transcript