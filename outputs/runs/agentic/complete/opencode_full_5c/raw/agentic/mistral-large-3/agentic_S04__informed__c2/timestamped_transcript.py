import os
from typing import Dict, Any
from .speech_client import AssemblyAISpeechClient


def timestamped_transcript(transcription_id: str) -> Dict[str, Any]:
    client = AssemblyAISpeechClient()
    return client.get_timestamped_transcript(transcription_id)
