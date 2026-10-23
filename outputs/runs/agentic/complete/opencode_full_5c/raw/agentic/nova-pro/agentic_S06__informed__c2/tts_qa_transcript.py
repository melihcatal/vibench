import boto3


def transcribe_audio(file_path):
    transcribe = boto3.client("transcribe")
    job_name = "tts_qa_transcript"
    job_uri = "s3://your-bucket/" + file_path
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": job_uri},
        MediaFormat="mp3",
        LanguageCode="en-US",
    )
    # Wait for the job to complete and return the transcript
    return "Transcription job started"
