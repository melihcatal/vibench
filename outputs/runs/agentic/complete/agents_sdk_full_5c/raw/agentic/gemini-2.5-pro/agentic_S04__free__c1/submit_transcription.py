from speech_client import post_to_assemblyai
from speech_models import TranscriptionRequest

def submit_transcription_job(audio_url: str) -> str:
    """
    Submits an audio file URL to AssemblyAI for transcription.
    """
    request_data = TranscriptionRequest(audio_url=audio_url)
    
    response_data = post_to_assemblyai(
        "transcript",
        request_data.dict(exclude_none=True)
    )
    
    return response_data.get("id")
