import os
from typing import Optional
import assemblyai as aai
from speech_models import SynthesisResponse

def _get_transcriber() -> aai.Transcriber:
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set")
    aai.settings.api_key = api_key
    return aai.Transcriber()

def transcribe_audio(response: SynthesisResponse) -> str:
    transcriber = _get_transcriber()
    
    with aai.tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
        temp_file.write(response.audio_bytes)
        temp_file_path = temp_file.name
    
    transcript = transcriber.transcribe(temp_file_path)
    return transcript.text