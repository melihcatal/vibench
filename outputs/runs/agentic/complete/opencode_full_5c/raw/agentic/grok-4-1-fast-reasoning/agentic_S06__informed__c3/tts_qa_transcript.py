import os
import tempfile
import assemblyai as aai
from typing import Optional


def transcribe_audio(audio_bytes: bytes) -> Optional[str]:
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable must be set")
    aai.settings.api_key = api_key
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
        tmp_file.write(audio_bytes)
        temp_path = tmp_file.name
    try:
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(temp_path)
        return transcript.text
    finally:
        os.unlink(temp_path)
