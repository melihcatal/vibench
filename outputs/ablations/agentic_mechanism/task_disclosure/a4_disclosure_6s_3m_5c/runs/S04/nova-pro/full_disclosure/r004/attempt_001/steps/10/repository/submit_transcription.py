import boto3

transcribe = boto3.client('transcribe')

def submit_transcription_job(job_name, media_file_uri, output_bucket_name):
    response = transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': media_file_uri},
        MediaFormat='mp3',
        LanguageCode='en-US',
        OutputBucketName=output_bucket_name
    )
    return response