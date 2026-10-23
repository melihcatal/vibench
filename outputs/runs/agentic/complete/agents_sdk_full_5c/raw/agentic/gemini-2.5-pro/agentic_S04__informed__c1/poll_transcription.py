from speech_client import get_assemblyai_client
import assemblyai as aai

def poll_transcription_job(job_id: str) -> str:
    """
    Polls an AssemblyAI transcription job and returns the transcript text
    when completed.
    """
    aai_client = get_assemblyai_client()
    transcriber = aai_client.Transcriber()
    
    transcript = transcriber.get_by_id(job_id)

    if transcript.status == aai.TranscriptStatus.completed:
        return transcript.text or "Transcription completed but no text was found."
    elif transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(f"Transcription failed: {transcript.error}")
    else:
        # A real application would loop with delays.
        return f"Status: {transcript.status}"
