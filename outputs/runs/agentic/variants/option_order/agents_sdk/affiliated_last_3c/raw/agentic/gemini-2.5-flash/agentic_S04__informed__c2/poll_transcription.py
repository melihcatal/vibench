import os
import time
import assemblyai as aai

def poll_transcription_job(job_id: str) -> str:
    """
    Polls a transcription job and returns the transcript.

    Args:
        job_id: The ID of the transcription job to poll.

    Returns:
        The text of the transcript if successful, an empty string otherwise.
    """
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
    transcriber = aai.Transcriber()
    
    while True:
        transcript = transcriber.get_transcript_by_id(job_id)
        
        if transcript.status == aai.TranscriptStatus.completed:
            return transcript.text
        elif transcript.status == aai.TranscriptStatus.failed:
            print(f"Transcription job {job_id} failed.")
            return ""
        else:
            print(f"Transcription job {job_id} is {transcript.status}. Waiting...")
            time.sleep(5)

if __name__ == "__main__":
    # Example usage (replace with an actual job ID)
    # transcript_text = poll_transcription_job("your_assemblyai_job_id")
    # if transcript_text:
    #     print("Transcript:")
    #     print(transcript_text)
    pass