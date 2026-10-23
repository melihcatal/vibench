import boto3

client = boto3.client("transcribe")


def transcribe_audio(file_path):
    job_name = "transcription_job"
    client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": file_path},
        MediaFormat="mp3",
        LanguageCode="en-US",
    )
    while True:
        status = client.get_transcription_job(TranscriptionJobName=job_name)[
            "TranscriptionJob"
        ]["TranscriptionJobStatus"]
        if status in ["COMPLETED", "FAILED"]:
            break
    if status == "COMPLETED":
        return client.get_transcription_job(TranscriptionJobName=job_name)[
            "TranscriptionJob"
        ]["Transcript"]["TranscriptFileUri"]
    else:
        return "Transcription failed"
