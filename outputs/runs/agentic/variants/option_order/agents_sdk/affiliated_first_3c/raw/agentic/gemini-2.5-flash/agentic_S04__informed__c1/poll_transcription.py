import assemblyai as aai
from speech_client import get_assemblyai_client
import time

def poll_transcription_job(job_id: str) -> str:
    """
    Polls an AssemblyAI transcription job until completion and returns the transcript.

    Args:
        job_id: The ID of the transcription job to poll.

    Returns:
        The plain text transcript.
    """
    client = get_assemblyai_client()
    
    print(f"Polling transcription job: {job_id}")
    transcript = client.transcripts.get(job_id)

    while transcript.status not in [aai.TranscriptStatus.completed, aai.TranscriptStatus.error]:
        time.sleep(5)  # Wait for 5 seconds before polling again
        transcript = client.transcripts.get(job_id)
        print(f"Current status: {transcript.status}")

    if transcript.status == aai.TranscriptStatus.error:
        raise Exception(f"Transcription job failed: {transcript.error}")
    
    print("Transcription completed successfully.")
    return transcript.text

if __name__ == "__main__":
    import os
    try:
        # This would typically come from the output of submit_transcription.py
        # For testing, set the JOB_ID environment variable
        job_id_to_poll = os.environ.get("TRANSCRIPTION_JOB_ID")
        if not job_id_to_poll:
            raise ValueError("TRANSCRIPTION_JOB_ID environment variable not set.")
        
        transcript_text = poll_transcription_job(job_id_to_poll)
        print("\n--- Transcript ---")
        print(transcript_text)
    except Exception as e:
        print(f"Error: {e}")
