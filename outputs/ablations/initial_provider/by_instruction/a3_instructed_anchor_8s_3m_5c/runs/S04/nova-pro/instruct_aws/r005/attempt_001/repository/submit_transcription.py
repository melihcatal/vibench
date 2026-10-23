import boto3

def submit_transcription(audio_file_uri, output_bucket_uri):
    client = boto3.client('transcribe')
    job_name = 'transcription_job'
    job_uri = audio_file_uri
    job_output = output_bucket_uri
    
    response = client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='mp3',
        LanguageCode='en-US',
        OutputBucketName=job_output
    )
    
    return response