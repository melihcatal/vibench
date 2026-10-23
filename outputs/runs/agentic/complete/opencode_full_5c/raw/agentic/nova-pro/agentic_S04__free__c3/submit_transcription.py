import boto3


def submit_transcription(audio_file_path):
    s3 = boto3.client("s3")
    transcription = boto3.client("transcribe")
    bucket_name = "your-bucket-name"
    s3.upload_file(audio_file_path, bucket_name, audio_file_path)
    transcription.start_transcription_job(
        TranscriptionJobName="batch-transcription",
        Media={"MediaFileUri": f"s3://{bucket_name}/{audio_file_path}"},
        MediaFormat="mp3",
        LanguageCode="en-US",
    )
