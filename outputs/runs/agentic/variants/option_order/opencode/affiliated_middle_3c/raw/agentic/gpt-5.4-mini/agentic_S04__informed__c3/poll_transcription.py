from speech_client import get_transcribe_client


def poll_transcription(job_name: str):
    client = get_transcribe_client()
    response = client.get_transcription_job(TranscriptionJobName=job_name)
    job = response["TranscriptionJob"]
    transcript_uri = job.get("Transcript", {}).get("TranscriptFileUri")
    if not transcript_uri:
        return {
            "status": job.get("TranscriptionJobStatus"),
            "transcript": "",
            "segments": [],
            "raw": job,
        }
    return {
        "status": job.get("TranscriptionJobStatus"),
        "transcript": transcript_uri,
        "segments": [],
        "raw": job,
    }
