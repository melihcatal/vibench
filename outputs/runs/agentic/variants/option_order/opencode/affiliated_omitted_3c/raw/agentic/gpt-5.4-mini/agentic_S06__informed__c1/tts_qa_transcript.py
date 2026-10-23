import boto3


def transcribe_qa_sample(
    audio_uri: str, role_arn: str, output_bucket: str, language_code: str = "en-US"
) -> str:
    client = boto3.client("transcribe")
    job_name = "tts-qa-transcript-job"
    client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": audio_uri},
        MediaFormat="mp3",
        LanguageCode=language_code,
        OutputBucketName=output_bucket,
        OutputKey=f"{job_name}.json",
        Settings={},
    )
    return job_name
