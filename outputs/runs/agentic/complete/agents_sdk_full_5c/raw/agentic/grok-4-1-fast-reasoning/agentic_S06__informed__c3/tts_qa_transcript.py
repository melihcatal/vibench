import os
import assemblyai as aai
from typing import Union

aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

def transcribe_audio(audio_path: str) -> str:
    """
    Transcribe synthesized QA audio sample using AssemblyAI.
    """
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_path)
    if not transcript.text:
        raise ValueError(f"Transcription failed: {transcript.error}")
    return transcript.text

def transcribe_audio_bytes(audio_bytes: bytes, sample_rate: int = 24000) -> str:
    """
    Transcribe from bytes (save temp file).
    """
    import tempfile
    import wave
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        with wave.open(tmp.name, "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(sample_rate)
            wav.writeframes(audio_bytes)
        return transcribe_audio(tmp.name)
