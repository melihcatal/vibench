import os
import assemblyai as aai
from typing import Optional

def transcribe_tts_audio(audio_bytes: bytes) -> Optional[str]:
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set")
    aai.settings.api_key = api_key
    transcriber = aai.Transcriber()
    config = aai.TranscriptionConfig(language_code="en")
    transcript = transcriber.transcribe(audio_bytes, config=config)
    if not transcript.text:
        return None
    return transcript.text