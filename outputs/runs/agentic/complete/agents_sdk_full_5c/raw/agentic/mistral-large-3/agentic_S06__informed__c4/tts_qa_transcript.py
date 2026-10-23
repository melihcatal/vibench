from typing import Dict, List
import os
import assemblyai as aai


def transcribe_audio(audio_url: str) -> str:
    """
    Transcribe synthesized QA samples to verify spoken output using AssemblyAI.
    """
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set")
    
    aai.settings.api_key = api_key
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_url)
    
    return transcript.text


def transcribe_audio_local(audio_path: str) -> str:
    """
    Transcribe local audio files using AssemblyAI.
    """
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set")
    
    aai.settings.api_key = api_key
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_path)
    
    return transcript.text