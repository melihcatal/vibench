import boto3


def transcribe_qa_transcript(audio_file):
    client = boto3.client('transcribe')
    job_name = 'qa_transcription_job'
    job_uri = 's3://your-bucket/' + audio_file
    client.start_transcription_job(
        TranscriptionJobName=job_name,
        LanguageCode='en-US',
        Media={'MediaFileUri': job_uri},
        OutputBucketName='your-bucket'
    )
    # Wait for the job to complete and return the transcript