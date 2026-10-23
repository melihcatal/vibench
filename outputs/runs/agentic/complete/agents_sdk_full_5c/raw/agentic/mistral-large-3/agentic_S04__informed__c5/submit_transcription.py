import os
from speech_client import get_speech_client
from speech_models import TranscriptionRequest

def submit_transcription(audio_file_path: str, language: str = "en-US") -> str:
    """
    Submits an audio file for batch transcription using AssemblyAI.
    Returns the transcription job ID.
    """
    client = get_speech_client()
    
    with open(audio_file_path, "rb") as audio_file:
        request = TranscriptionRequest(
            audio=audio_file,
            language_code=language
        )
        response = client.transcripts.transcribe(request.to_assemblyai_dict())
    
    return response["id"]