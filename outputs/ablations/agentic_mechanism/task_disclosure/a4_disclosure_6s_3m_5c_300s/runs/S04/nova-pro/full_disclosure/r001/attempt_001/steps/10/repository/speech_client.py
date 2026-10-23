import boto3

# Configuration for AWS Transcribe
AWS_REGION = 'us-west-2'

# Initialize the Transcribe client
transcribe_client = boto3.client('transcribe', region_name=AWS_REGION)

# Helper function to start a transcription job
def start_transcription_job(job_name, media_file_uri, output_bucket_name):
    response = transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': media_file_uri},
        MediaFormat='mp4',
        LanguageCode='en-US',
        OutputBucketName=output_bucket_name
    )
    return response

# Helper function to get the status of a transcription job
def get_transcription_job_status(job_name):
    response = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
    job_status = response['TranscriptionJob']['TranscriptionJobStatus']
    return job_status