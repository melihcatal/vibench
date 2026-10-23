import boto3


def timestamped_transcript(job_name):
    client = boto3.client("transcribe")
    response = client.get_transcription_job(TranscriptionJobName=job_name)
    if response["TranscriptionJob"]["TranscriptionJobStatus"] == "COMPLETED":
        transcript_uri = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
        with open("transcript.json", "w") as f:
            f.write(response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"])
        return transcript_uri
    else:
        return None
