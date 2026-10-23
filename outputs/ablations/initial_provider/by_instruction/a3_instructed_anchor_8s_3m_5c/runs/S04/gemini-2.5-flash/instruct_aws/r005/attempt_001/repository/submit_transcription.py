import boto3
from speech_client import get_transcribe_client
from speech_models import TranscriptionJobRequest

def submit_transcription_job(job_request: TranscriptionJobRequest) -> dict:
    transcribe_client = get_transcribe_client()
    response = transcribe_client.start_transcription_job(
        TranscriptionJobName=job_request.job_name,
        MediaFormat=job_request.media_format,
        Media={'MediaFileUri': job_request.audio_file_uri},
        LanguageCode=job_request.language_code
    )
    return response['TranscriptionJob']

if __name__ == '__main__':
    # This is a placeholder for actual usage. In a real scenario, you'd get
    # these values from environment variables, configuration, or command line arguments.
    # Ensure your AWS credentials are configured (e.g., via AWS CLI or environment variables).
    # The S3 URI should point to an audio file in an S3 bucket that Transcribe can access.
    example_request = TranscriptionJobRequest(
        job_name="my-batch-transcription-job-1",
        audio_file_uri="s3://your-s3-bucket/your-audio-file.wav",
        media_format="wav",
        language_code="en-US"
    )
    try:
        job_info = submit_transcription_job(example_request)
        print(f"Transcription job submitted: {job_info['TranscriptionJobStatus']} - {job_info['TranscriptionJobName']}")
        print(f"Job ARN: {job_info['TranscriptionJobArn']}")
    except Exception as e:
        print(f"Error submitting transcription job: {e}")
