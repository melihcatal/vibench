from speech_client import get_assemblyai_client

def poll_transcription(job_id: str) -> str:
    """
    Poll an AssemblyAI transcription job and return the transcript text if completed.
    Raises ValueError if the job fails or is not found.
    """
    client = get_assemblyai_client()
    transcript = client.transcripts.get(job_id)
    if transcript.status == "completed":
        return transcript.text
    elif transcript.status == "error":
        raise ValueError(f"Transcription job failed: {transcript.error}")
    else:
        raise ValueError(f"Transcription job not completed. Status: {transcript.status}")