import boto3


def transcribe_tts_qa_sample(audio_file):
    transcribe_client = boto3.client("transcribe")
    job_name = "tts_qa_transcription"
    job_uri = f"s3://your-bucket/{audio_file}"
    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": job_uri},
        MediaFormat="mp3",
        LanguageCode="en-US",
    )
    return job_name
