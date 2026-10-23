import assemblyai as aai
import os
from speech_client import get_assemblyai_client


def poll_transcription_job(transcript_id: str) -> aai.Transcript:
    """
    Polls a transcription job and returns the transcript.
    """
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
    client = get_assemblyai_client()

    transcript = client.transcripts.get(transcript_id)
    return transcript
