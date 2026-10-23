import os
import assemblyai as aai
from typing import Optional

def transcribe_audio_file(audio_file_path: str) -> Optional[str]:
    """
    Transcribes a synthesized audio file to verify its content using AssemblyAI.

    Args:
        audio_file_path: The local path to the audio file.

    Returns:
        The transcribed text as a string, or None if transcription fails.
    """
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")

    aai.settings.api_key = api_key

    transcriber = aai.Transcriber()
    
    transcript = transcriber.transcribe(audio_file_path)

    if transcript.status == aai.TranscriptStatus.error:
        print(f"Transcription failed: {transcript.error}")
        return None
    
    return transcript.text
