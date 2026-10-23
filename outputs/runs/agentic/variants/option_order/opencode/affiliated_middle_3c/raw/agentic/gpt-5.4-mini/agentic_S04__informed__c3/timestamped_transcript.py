from speech_client import get_transcribe_client


def timestamped_transcript(job_name: str, word_level: bool = True):
    client = get_transcribe_client()
    response = client.get_transcription_job(TranscriptionJobName=job_name)
    job = response["TranscriptionJob"]
    transcript_uri = job.get("Transcript", {}).get("TranscriptFileUri")
    return {
        "status": job.get("TranscriptionJobStatus"),
        "transcript": transcript_uri,
        "segments": [{"word_level": word_level}],
        "raw": job,
    }
