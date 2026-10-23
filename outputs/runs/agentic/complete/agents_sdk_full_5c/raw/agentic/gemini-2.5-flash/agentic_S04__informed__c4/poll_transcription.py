import os
import time
import assemblyai as aai

def poll_transcription_job(job_id: str):
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
    transcriber = aai.Transcriber()

    print(f"Polling transcription job with ID: {job_id}")
    while True:
        transcript = transcriber.get_transcript(job_id)
        if transcript.status == aai.TranscriptStatus.completed:
            print("Transcription completed.")
            return transcript.text
        elif transcript.status == aai.TranscriptStatus.failed:
            print(f"Transcription failed: {transcript.error}")
            return None
        else:
            print(f"Transcription status: {transcript.status}. Waiting...")
            time.sleep(5) # Wait for 5 seconds before polling again

if __name__ == "__main__":
    # Example usage (replace with actual job ID)
    # Ensure ASSEMBLYAI_API_KEY is set in your environment
    # job_id = "YOUR_TRANSCRIPTION_JOB_ID"
    # transcript_text = poll_transcription_job(job_id)
    # if transcript_text:
    #     print("\nFull Transcript:")
    #     print(transcript_text)
    pass
