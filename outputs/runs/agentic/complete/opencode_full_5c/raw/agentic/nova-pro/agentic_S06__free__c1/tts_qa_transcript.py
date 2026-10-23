import boto3


def transcribe_qa_samples(audio_file):
    transcribe_client = boto3.client("transcribe")
    job_name = "qa-transcription-job"
    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": audio_file},
        MediaFormat="mp3",
        LanguageCode="en-US",
    )
    return job_name
