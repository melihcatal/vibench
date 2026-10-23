import boto3

transcribe = boto3.client("transcribe", region_name="us-west-2")


def poll_transcription(job_name):
    response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    job_status = response["TranscriptionJob"]["TranscriptionJobStatus"]
    if job_status in ["COMPLETED", "FAILED"]:
        return response["TranscriptionJob"]["Transcript"]
    else:
        return "Job is still in progress"
