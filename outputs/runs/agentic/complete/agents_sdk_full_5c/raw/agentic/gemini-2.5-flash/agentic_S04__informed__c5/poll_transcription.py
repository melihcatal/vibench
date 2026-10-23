import os
import assemblyai

def poll_transcription_job(transcript_id: str) -> assemblyai.Transcript:
    """Polls an AssemblyAI transcription job and returns the transcript."""
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")

    transcriber = assemblyai.Transcriber(api_key)
    transcript = transcriber.get_transcript_by_id(transcript_id)
    return transcript
