import os
from speech_client import SpeechClient
from speech_models import TranscriptionJob

def submit_transcription(job: TranscriptionJob):
    client = SpeechClient().get_client()
    try:
        response = client.start_transcription_job(
            TranscriptionJobName=job.job_name,
            LanguageCode=job.language_code,
            MediaFormat=job.media_uri.split('.')[-1], # Infer format from URI
            Media={ 'MediaFileUri': job.media_uri },
            OutputBucketName=job.output_bucket # AWS Transcribe specific output
        )
        return response
    except Exception as e:
        print(f"Error submitting transcription job: {e}")
        return None

if __name__ == '__main__':
    # Example usage (requires AWS credentials and S3 URI)
    # Set environment variables: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
    # Example S3 URI: s3://your-bucket/your-audio-file.mp3
    example_job = TranscriptionJob(
        job_name="my-test-transcription-job",
        media_uri="s3://your-bucket-name/your-audio-file.mp3",
        language_code="en-US",
        output_bucket="your-transcription-output-bucket"
    )
    # Make sure the S3 bucket exists and is accessible by Transcribe
    # Also, ensure the IAM role used has permissions to read from media_uri and write to output_bucket
    response = submit_transcription(example_job)
    if response:
        print(f"Transcription job submitted: {response['TranscriptionJob']['TranscriptionJobName']}")
    else:
        print("Failed to submit transcription job.")
