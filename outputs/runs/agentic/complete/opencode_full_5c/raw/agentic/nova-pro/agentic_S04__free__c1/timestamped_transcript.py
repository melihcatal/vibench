import boto3

transcribe = boto3.client("transcribe", region_name="us-west-2")


def get_timestamped_transcript(job_name):
    response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    if response["TranscriptionJob"]["TranscriptionJobStatus"] == "COMPLETED":
        transcript_uri = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
        # Additional logic to extract timestamps from transcript
        return "Timestamps extracted"
    else:
        return None
