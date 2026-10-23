import os
import time
from speech_client import get_speech_client
from speech_models import normalize_transcript_response, TranscriptionResult

def poll_for_transcript(job_id: str) -> TranscriptionResult:
    """
    Polls AssemblyAI for the result of a transcription job.

    Args:
        job_id: The ID of the transcription job.

    Returns:
        The completed transcription result.
    """
    client = get_speech_client()
    transcriber = client.Transcriber()
    
    while True:
        job = transcriber.get(job_id)
        
        if job.status == 'completed':
            print("Transcription job completed.")
            return normalize_transcript_response(job)
        elif job.status == 'failed':
            print(f"Transcription job failed: {job.error}")
            return normalize_transcript_response(job)
        
        print(f"Job status: {job.status}. Polling again in 5 seconds...")
        time.sleep(5)

if __name__ == '__main__':
    job_id_from_env = os.getenv("TRANSCRIPTION_ID")
    if not job_id_from_env:
        print("Please set the TRANSCRIPTION_ID environment variable.")
    else:
        result = poll_for_transcript(job_id_from_env)
        if result.status == 'completed':
            print("\nTranscript:")
            print(result.text)
