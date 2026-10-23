from speech_client import get_assemblyai_client
import assemblyai

def submit_transcription_job(audio_url: str) -> str:
    """
    Submits an audio file for batch transcription to AssemblyAI.
    """
    client = get_assemblyai_client()
    transcriber = client.transcriber
    
    config = assemblyai.TranscriptionConfig()

    job = transcriber.submit(audio_url, config)
    
    return job.id
