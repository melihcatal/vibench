import boto3


def poll_transcription(job_name):
    client = boto3.client("transcribe")
    while True:
        response = client.get_transcription_job(TranscriptionJobName=job_name)
        job_status = response["TranscriptionJob"]["TranscriptionJobStatus"]
        if job_status in ["COMPLETED", "FAILED"]:
            return response
        print("Waiting for transcription...")
        time.sleep(10)
