import os
from speech_client import get_transcribe_client, get_s3_client

def diarized_transcript(audio_file_path: str, bucket_name: str, file_key: str, max_speaker_labels: int = 2):
    s3_client = get_s3_client()
    # Ensure the file is in S3 if it's a local path
    if not audio_file_path.startswith("s3://"):
        s3_client.upload_file(audio_file_path, bucket_name, file_key)
        media_file_uri = f"s3://{bucket_name}/{file_key}"
    else:
        media_file_uri = audio_file_path
        # Extract bucket_name and file_key from S3 URI if provided directly
        # For simplicity, assuming bucket_name and file_key are provided correctly
        # or extracted upstream if audio_file_path is already an S3 URI.

    transcribe_client = get_transcribe_client()
    job_name = os.path.splitext(file_key)[0].replace("/", "-") + "-diarization-job"
    media_format = audio_file_path.split('.')[-1] if not audio_file_path.startswith("s3://") else "mp3" # Defaulting to mp3 if S3 URI and format not explicit

    response = transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': media_file_uri},
        MediaFormat=media_format,
        LanguageCode='en-US',
        Settings={'ShowSpeakerLabels': True, 'MaxSpeakerLabels': max_speaker_labels}
    )
    return response['TranscriptionJob']['TranscriptionJobName']
