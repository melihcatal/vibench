import os
import assemblyai

def get_transcriber():
    """Initializes and returns the AssemblyAI client."""
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")
    
    assemblyai.settings.api_key = api_key
    transcriber = assemblyai.Transcriber()
    return transcriber

def get_transcript_by_id(job_id: str):
    """Retrieves a transcript object by its ID."""
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")
    assemblyai.settings.api_key = api_key
    return assemblyai.Transcript.get_by_id(job_id)
