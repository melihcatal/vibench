import boto3


def transcribe_qa_samples(audio_file_path):
    transcribe_client = boto3.client("transcribe")
    job_name = "qa-transcription-job"
    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": audio_file_path},
        MediaFormat="mp3",
        LanguageCode="en-US",
    )
    while True:
        status = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)[
            "TranscriptionJob"
        ]["TranscriptionJobStatus"]
        if status in ["COMPLETED", "FAILED"]:
            break
    if status == "COMPLETED":
        transcript_uri = transcribe_client.get_transcription_job(
            TranscriptionJobName=job_name
        )["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
        response = requests.get(transcript_uri)
        return response.text
    else:
        return "Transcription failed"
