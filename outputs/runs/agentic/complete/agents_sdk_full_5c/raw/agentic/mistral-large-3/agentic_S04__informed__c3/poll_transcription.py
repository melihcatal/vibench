from speech_client import get_speech_client

def poll_transcription(job_id: str) -> str:
    """
    Polls AssemblyAI for the status of a transcription job.
    Returns the transcript text if completed.
    """
    client = get_speech_client()
    transcript = client.transcripts.get(job_id)
    
    if transcript.status == "completed":
        return transcript.text
    elif transcript.status == "failed":
        raise ValueError(f"Transcription job failed: {transcript.error}")
    else:
        raise ValueError(f"Transcription job not completed. Current status: {transcript.status}")