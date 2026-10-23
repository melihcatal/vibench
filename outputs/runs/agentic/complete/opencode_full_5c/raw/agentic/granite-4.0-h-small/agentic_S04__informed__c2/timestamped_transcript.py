import os
import json
from assemblyai import AssemblyAI

# Load API key from environment
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")

aai = AssemblyAI(ASSEMBLYAI_API_KEY)


def request_timestamped_transcript(audio_path: str) -> str:
    """Submit audio for transcription requesting word-level timestamps.
    Returns the job ID for later polling.
    """
    response = aai.transcript.upload(
        {
            "audio_url": audio_path,
            "config": {"timestamps": "words", "speaker_diarization": False},
        }
    )
    return response["id"]
