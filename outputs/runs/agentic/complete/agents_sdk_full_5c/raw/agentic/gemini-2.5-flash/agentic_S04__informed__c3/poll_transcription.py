import os
import assemblyai as aai
from speech_client import get_assemblyai_client
from speech_models import TranscriptionJob

def poll_transcription_job(job_id: str) -> TranscriptionJob:
    """
    Polls an AssemblyAI transcription job and returns its status and result.
    """
    client = get_assemblyai_client()
    
    transcriber = aai.Transcriber()
    
    # Retrieve the transcript object by ID
    transcript = transcriber.get_transcript_by_id(job_id)
    
    job_status = transcript.status
    transcript_text = None
    
    if job_status == aai.TranscriptStatus.completed:
        transcript_text = transcript.text
    
    return TranscriptionJob(
        id=transcript.id,
        status=job_status,
        transcript=transcript_text
    )

if __name__ == "__main__":
    # Example usage: replace with a real job ID
    # This requires a job to have been submitted first via submit_transcription.py
    job_to_poll = "YOUR_ASSEMBLYAI_JOB_ID" 

    if not os.getenv("ASSEMBLYAI_API_KEY"):
        print("Please set the ASSEMBLYAI_API_KEY environment variable.")
    elif job_to_poll == "YOUR_ASSEMBLYAI_JOB_ID":
        print("Please replace 'YOUR_ASSEMBLYAI_JOB_ID' with an actual job ID.")
    else:
        result = poll_transcription_job(job_to_poll)
        print(f"Job ID: {result.id}")
        print(f"Status: {result.status}")
        if result.transcript:
            print(f"Transcript: {result.transcript[:200]}...") # Print first 200 chars
