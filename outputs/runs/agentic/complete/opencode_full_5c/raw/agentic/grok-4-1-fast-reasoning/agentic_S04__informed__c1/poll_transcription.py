import os
import time
from typing import Any
from assemblyai import Client
from speech_client import poll_transcript


def poll_transcription(job_id: str) -> str:
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    client = Client(api_key=api_key)
    transcript = poll_transcript(client, job_id)
    return transcript.text
