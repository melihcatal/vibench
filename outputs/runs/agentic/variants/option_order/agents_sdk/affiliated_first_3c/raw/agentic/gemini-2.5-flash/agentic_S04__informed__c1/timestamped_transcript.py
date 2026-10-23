import assemblyai as aai
from speech_client import get_assemblyai_client
import os

def get_timestamped_transcript(job_id: str) -> aai.Transcript:
    """
    Retrieves a completed AssemblyAI transcription job with word-level timestamps.

    Args:
        job_id: The ID of the completed transcription job.

    Returns:
        The AssemblyAI Transcript object containing words with timestamps.
    """
    client = get_assemblyai_client()
    
    print(f"Retrieving timestamped transcript for job: {job_id}")
    transcript = client.transcripts.get(job_id)

    if transcript.status == aai.TranscriptStatus.error:
        raise Exception(f"Transcription job failed or not found: {transcript.error}")
    elif transcript.status != aai.TranscriptStatus.completed:
        raise Exception(f"Transcription job {job_id} is not yet completed. Current status: {transcript.status}")

    print("Transcript retrieved with timestamps.")
    return transcript

if __name__ == "__main__":
    try:
        # This would typically come from a completed transcription job
        # For testing, set the COMPLETED_JOB_ID environment variable
        completed_job_id = os.environ.get("COMPLETED_JOB_ID")
        if not completed_job_id:
            raise ValueError("COMPLETED_JOB_ID environment variable not set.")
        
        transcript_obj = get_timestamped_transcript(completed_job_id)
        print("\n--- Timestamped Transcript (first 10 words) ---")
        for word in transcript_obj.words[:10]:
            print(f"Word: {word.text}, Start: {word.start}, End: {word.end}")
        
        # You can also get paragraphs with timestamps
        print("\n--- Paragraphs with Timestamps (first 2 paragraphs) ---")
        for paragraph in transcript_obj.get_paragraphs()[:2]:
            print(f"Start: {paragraph.start}, End: {paragraph.end}")
            print(paragraph.text)

    except Exception as e:
        print(f"Error: {e}")
