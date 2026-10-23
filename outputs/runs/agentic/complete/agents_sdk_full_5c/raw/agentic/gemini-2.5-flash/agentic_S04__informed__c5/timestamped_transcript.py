import os
import assemblyai

def get_timestamped_transcript(transcript_id: str) -> assemblyai.Transcript:
    """Retrieves an AssemblyAI transcript with word-level timestamps."""
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")

    transcriber = assemblyai.Transcriber(api_key)
    # AssemblyAI automatically includes word-level timestamps in the transcript object
    transcript = transcriber.get_transcript_by_id(transcript_id)
    return transcript
