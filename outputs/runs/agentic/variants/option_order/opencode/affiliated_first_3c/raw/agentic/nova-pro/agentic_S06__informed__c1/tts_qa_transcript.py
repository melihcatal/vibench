import boto3


def transcribe_audio(file_path):
    transcribe_client = boto3.client("transcribe")
    job_name = "transcription_job"
    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": file_path},
        MediaFormat="mp3",
        LanguageCode="en-US",
    )
    while True:
        status = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        if status["TranscriptionJob"]["TranscriptionJobStatus"] in [
            "COMPLETED",
            "FAILED",
        ]:
            break
    if status["TranscriptionJob"]["TranscriptionJobStatus"] == "COMPLETED":
        transcript_uri = status["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
        response = transcribe_client.get_transcription_job(
            TranscriptionJobName=job_name
        )
        return response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
    else:
        return "Transcription failed"
