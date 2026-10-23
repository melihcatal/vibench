from speech_client import transcribe_client


def timestamped_transcript(job_name):
    response = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
    if response["TranscriptionJob"]["TranscriptionJobStatus"] == "COMPLETED":
        transcript_uri = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
        # Additional logic to process timestamps
        return transcript_uri
    else:
        return None
