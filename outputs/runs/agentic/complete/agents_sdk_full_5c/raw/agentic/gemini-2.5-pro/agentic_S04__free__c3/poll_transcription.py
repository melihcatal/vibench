import time
import os
from speech_client import get_assemblyai_session

def poll_for_transcript(job_id: str) -> dict:
    """Polls an AssemblyAI transcription job until it's completed."""
    session = get_assemblyai_session()
    url = f"https://api.assemblyai.com/v2/transcript/{job_id}"
    
    while True:
        response = session.get(url)
        response.raise_for_status()
        result = response.json()
        
        if result["status"] == "completed":
            return result
        elif result["status"] == "error":
            raise RuntimeError(f"Transcription failed: {result['error']}")
        
        print("Job is not complete. Waiting...")
        time.sleep(5)

def get_transcript_text(job_id: str) -> str:
    """Gets the final transcript text for a completed job."""
    result = poll_for_transcript(job_id)
    return result.get("text")
