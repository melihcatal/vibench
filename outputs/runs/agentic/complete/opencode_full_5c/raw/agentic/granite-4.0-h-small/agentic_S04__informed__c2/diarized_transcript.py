import os
import json
from assemblyai import AssemblyAI

# Load API key from environment
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")

# Init client once
aai = AssemblyAI(ASSEMBLYAI_API_KEY)


def request_diarized_transcript(audio_path: str) -> str:
    """Submit audio for transcription with speaker diarization.
    Returns the job ID for later polling.
    """
    response = aai.transcript.upload(
        {
            "audio_url": audio_path,
            "config": {
                "speaker_diarization": True,
                "speaker_count": 2,  # optional, adjust as needed
                "timestamps": "words",
            },
        }
    )
    return response["id"]
