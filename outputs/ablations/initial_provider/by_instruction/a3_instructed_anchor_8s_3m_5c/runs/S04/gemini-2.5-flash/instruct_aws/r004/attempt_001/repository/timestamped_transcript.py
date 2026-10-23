import os
from speech_client import get_transcribe_client, get_s3_client

def timestamped_transcript(audio_file_path: str, bucket_name: str, file_key: str):
    s3_client = get_s3_client()
    if not audio_file_path.startswith("s3://"):
        s3_client.upload_file(audio_file_path, bucket_name, file_key)
        media_file_uri = f"s3://{bucket_name}/{file_key}"
    else:
        media_file_uri = audio_file_path

    transcribe_client = get_transcribe_client()
    job_name = os.path.splitext(file_key)[0].replace("/", "-") + "-timestamp-job"
    media_format = audio_file_path.split('.')[-1] if not audio_file_path.startswith("s3://") else "mp3"

    response = transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': media_file_uri},
        MediaFormat=media_format,
        LanguageCode='en-US',
        Settings={'ShowWordTimeStamps': True}
    )
    return response['TranscriptionJob']['TranscriptionJobName']
