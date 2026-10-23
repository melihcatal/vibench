import assemblyai
from speech_client import assemblyai_client
from speech_models import TranscriptionJob

def submit_audio_for_transcription(audio_url: str) -> TranscriptionJob:
    """
    Submits an audio file URL for batch transcription using AssemblyAI.

    Args:
        audio_url: The publicly accessible URL of the audio file.

    Returns:
        A TranscriptionJob object with the job ID and status.
    """
    config = assemblyai.TranscriptionConfig()
    
    transcript = assemblyai_client.submit(audio_url, config)
    
    return TranscriptionJob(
        job_id=transcript.id,
        status=transcript.status,
        audio_url=audio_url
    )
