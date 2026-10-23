import boto3


def poll_transcription(job_name):
    transcription = boto3.client("transcribe")
    response = transcription.get_transcription_job(TranscriptionJobName=job_name)
    status = response["TranscriptionJob"]["TranscriptionJobStatus"]
    if status in ["COMPLETED", "FAILED"]:
        return response
    else:
        return "In progress"
