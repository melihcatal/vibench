import boto3


def transcribe_tts_qa_sample(audio_file_path):
    transcribe = boto3.client("transcribe")
    job_name = "tts_qa_transcription_job"
    job_uri = f"s3://YOUR_BUCKET_NAME/{audio_file_path}"
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": job_uri},
        MediaFormat="mp3",
        LanguageCode="en-US",
    )
    return job_name
