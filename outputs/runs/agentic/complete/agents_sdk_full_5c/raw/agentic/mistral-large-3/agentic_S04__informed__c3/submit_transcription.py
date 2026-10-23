import os
from speech_client import get_speech_client
from speech_models import TranscriptionRequest

def submit_transcription(audio_file_path: str, language_code: str = "en-US") -> str:
    """
    Submits an audio file to AssemblyAI for batch transcription.
    Returns the transcription job ID.
    """
    client = get_speech_client()
    
    with open(audio_file_path, "rb") as audio_file:
        request = TranscriptionRequest(
            audio_file=audio_file,
            language_code=language_code
        )
        response = client.transcripts.transcribe(request.to_dict())
    
    return response["id"]