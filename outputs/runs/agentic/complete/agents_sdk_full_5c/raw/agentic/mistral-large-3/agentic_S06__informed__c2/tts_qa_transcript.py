import os
import assemblyai as aai
from typing import Optional


def transcribe_audio(audio_url: str) -> Optional[str]:
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
    transcriber = aai.Transcriber()
    
    transcript = transcriber.transcribe(audio_url)
    if transcript.status == aai.TranscriptStatus.error:
        return None
    
    return transcript.text