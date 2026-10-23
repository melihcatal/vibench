import boto3

transcribe_client = boto3.client("transcribe")


def timestamped_transcript(job_name):
    response = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
    return response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
