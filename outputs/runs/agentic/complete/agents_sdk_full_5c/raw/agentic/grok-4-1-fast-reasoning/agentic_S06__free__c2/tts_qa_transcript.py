import os
import tempfile
from openai import OpenAI

def transcribe_tts_audio(audio_bytes: bytes) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if not client.api_key:
        raise ValueError("OPENAI_API_KEY must be set.")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_file.write(audio_bytes)
        tmp_path = tmp_file.name
    
    try:
        with open(tmp_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=("qa_audio.mp3", audio_file)
            )
        return transcription.text
    finally:
        os.unlink(tmp_path)
