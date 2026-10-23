import os
import assemblyai as aai
from typing import Optional

def get_speech_client() -> aai.Client:
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable is not set")
    return aai.Client(api_key=api_key)

def upload_audio(client: aai.Client, file_path: str) -> str:
    """Upload local audio file and return the upload URL."""
    return client.upload(file_path)
