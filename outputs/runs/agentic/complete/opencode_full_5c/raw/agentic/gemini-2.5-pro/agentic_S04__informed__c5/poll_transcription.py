from speech_client import get_speech_client


def poll_transcription_job(job_id: str) -> str:
    aai = get_speech_client()
    transcript = aai.Transcript.get_by_id(job_id)
    while transcript.status not in ["completed", "error"]:
        transcript = transcript.poll()

    if transcript.status == "error":
        return f"Transcription failed: {transcript.error}"

    return transcript.text
