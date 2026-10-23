import boto3


def poll_transcription(job_name):
    client = boto3.client("transcribe")
    response = client.get_transcription_job(TranscriptionJobName=job_name)
    while response["TranscriptionJob"]["TranscriptionJobStatus"] != "COMPLETED":
        time.sleep(10)
        response = client.get_transcription_job(TranscriptionJobName=job_name)
    return response["TranscriptionJob"]["Transcript"]
