from speech_client import get_speech_client

def poll_transcription(job_id: str) -> str:
    """
    Polls an AssemblyAI transcription job and returns the transcript text.
    Raises an exception if the job fails.
    """
    client = get_speech_client()
    
    transcript = client.transcripts.get(job_id)
    
    if transcript.status == "completed":
        return transcript.text
    elif transcript.status == "failed":
        raise Exception(f"Transcription job failed: {transcript.error}")
    else:
        raise Exception(f"Transcription job not completed. Current status: {transcript.status}")