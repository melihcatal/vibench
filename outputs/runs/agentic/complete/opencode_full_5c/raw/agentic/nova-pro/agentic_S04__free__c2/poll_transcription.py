import boto3

transcribe_client = boto3.client("transcribe")


def poll_transcription(transcription_job_name):
    response = transcribe_client.get_transcription_job(
        TranscriptionJobName=transcription_job_name
    )
    job_status = response["TranscriptionJob"]["TranscriptionJobStatus"]
    if job_status in ["COMPLETED", "FAILED"]:
        return response["TranscriptionJob"]["Transcript"]
    else:
        return None
