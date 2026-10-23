import boto3


def timestamped_transcript(job_name):
    transcription = boto3.client("transcribe")
    response = transcription.get_transcription_job(TranscriptionJobName=job_name)
    if response["TranscriptionJob"]["TranscriptionJobStatus"] == "COMPLETED":
        return response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
    else:
        return "Job not completed"
