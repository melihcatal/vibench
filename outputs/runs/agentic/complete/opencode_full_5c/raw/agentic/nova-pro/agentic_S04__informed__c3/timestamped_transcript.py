import boto3


def timestamped_transcript(job_name):
    client = boto3.client("transcribe")
    response = client.get_transcription_job(TranscriptionJobName=job_name)
    return response["TranscriptionJob"]["TranscriptionJobStatus"]
