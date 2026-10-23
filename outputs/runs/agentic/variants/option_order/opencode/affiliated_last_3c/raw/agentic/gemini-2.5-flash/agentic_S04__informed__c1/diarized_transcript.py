import assemblyai as aai
import os
from speech_client import get_assemblyai_client


def request_diarized_transcript(audio_url: str) -> aai.Transcript:
    """
    Requests speaker diarization for a recorded meeting using AssemblyAI.
    """
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
    client = get_assemblyai_client()

    config = aai.TranscriptionConfig(speaker_diarization=True)
    transcript = client.transcripts.submit(audio_url=audio_url, config=config)
    return transcript
