from speech_client import get_assemblyai_client
from speech_models import TranscriptionJob
import assemblyai as aai

def submit_transcription_job(audio_url: str) -> TranscriptionJob:
    """
    Submits a new transcription job to AssemblyAI.
    """
    aai_client = get_assemblyai_client()
    transcriber = aai_client.Transcriber()
    config = aai.TranscriptionConfig()
    
    transcript = transcriber.submit(audio_url, config)
    
    return TranscriptionJob(id=transcript.id, status=str(transcript.status))
