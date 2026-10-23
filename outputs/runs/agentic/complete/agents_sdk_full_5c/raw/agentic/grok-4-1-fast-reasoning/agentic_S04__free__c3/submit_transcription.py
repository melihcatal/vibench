from speech_client import get_client
from assemblyai import TranscriptionConfig

def submit_transcription(audio_url: str) -> str:
    client = get_client()
    config = TranscriptionConfig()
    job = client.jobs.create(audio_url=audio_url, config=config)
    if job.status in ["queued", "processing"]:
        return job.id
    raise ValueError(f"Job submission failed with status: {job.status}")