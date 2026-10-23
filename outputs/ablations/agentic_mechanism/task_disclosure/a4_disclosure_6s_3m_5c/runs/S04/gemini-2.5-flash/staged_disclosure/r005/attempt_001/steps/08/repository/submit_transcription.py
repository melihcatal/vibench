import boto3
import os

def submit_transcription_job(bucket_name, file_key, job_name, media_format, language_code):
    """
    Submits an audio file for batch transcription using AWS Transcribe.

    Args:
        bucket_name (str): The name of the S3 bucket where the audio file is stored.
        file_key (str): The key (path) of the audio file in the S3 bucket.
        job_name (str): A unique name for the transcription job.
        media_format (str): The format of the audio file (e.g., 'mp3', 'flac').
        language_code (str): The language code of the audio in the file (e.g., 'en-US').

    Returns:
        dict: The response from the AWS Transcribe service.
    """
    transcribe_client = boto3.client('transcribe', region_name=os.environ.get('AWS_REGION', 'us-east-1'))

    media_file_uri = f"s3://{bucket_name}/{file_key}"

    response = transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': media_file_uri},
        MediaFormat=media_format,
        LanguageCode=language_code
    )
    return response

if __name__ == "__main__":
    # Example usage:
    # Ensure you have AWS credentials configured and the audio file in S3.
    # Replace with your S3 bucket, file key, and desired job name.
    s3_bucket = "your-s3-bucket-name"
    audio_file_key = "audio/your-audio-file.mp3"
    transcription_job_name = "my-first-transcription-job"
    audio_media_format = "mp3"  # or 'flac', 'wav', etc.
    audio_language_code = "en-US" # or 'es-US', 'fr-CA', etc.

    print(f"Submitting transcription job '{transcription_job_name}' for s3://{s3_bucket}/{audio_file_key}...")
    try:
        response = submit_transcription_job(
            s3_bucket,
            audio_file_key,
            transcription_job_name,
            audio_media_format,
            audio_language_code
        )
        print("Transcription job submitted successfully:")
        print(response)
    except Exception as e:
        print(f"Error submitting transcription job: {e}")
