import os
from typing import Optional
from assemblyai import Client


def get_speech_client(api_key: Optional[str] = None) -> Client:
    api_key = api_key or os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable must be set")
    return Client(api_key=api_key)
