import boto3

transcribe = boto3.client("transcribe", region_name="us-west-2")


def diarize_transcription(job_name):
    response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    if response["TranscriptionJob"]["TranscriptionJobStatus"] == "COMPLETED":
        transcript_uri = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
        # Additional logic to process transcript for diarization
        return "Diarization processed"
    else:
        return None
