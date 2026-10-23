import os
import time
from typing import Any
from assemblyai import Client
from speech_client import poll_transcript
from speech_models import get_basic_config


def submit_transcription(audio_file: str) -> str:
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    client = Client(api_key=api_key)
    config = get_basic_config()
    upload_url = client.upload(audio_file)
    transcript = client.transcripts.create(upload_url, config)
    return transcript.id
