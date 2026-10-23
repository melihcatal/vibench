import os
from typing import Optional
import assemblyai as aai

def transcribe_synthesized_audio(
    audio_url: Optional[str] = None,
    audio_file_path: Optional[str] = None
) -> str:
    """
    Transcribe synthesized QA samples to verify spoken output using AssemblyAI.
    """
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("AssemblyAI API key must be provided.")
    
    aai.settings.api_key = api_key
    transcriber = aai.Transcriber()
    
    if audio_url:
        transcript = transcriber.transcribe(audio_url)
    elif audio_file_path:
        transcript = transcriber.transcribe(audio_file_path)
    else:
        raise ValueError("Either audio_url or audio_file_path must be provided.")
    
    if transcript.status == aai.TranscriptStatus.error:
        raise Exception(f"Transcription failed: {transcript.error}")
    
    return transcript.text