from speech_client import get_client
from assemblyai import TranscriptionConfig

def diarized_transcript(audio_url: str) -> str:
    client = get_client()
    config = TranscriptionConfig(speaker_labels=True)
    job = client.jobs.create(audio_url=audio_url, config=config)
    if job.status in ["queued", "processing"]:
        return job.id
    raise ValueError(f"Job submission failed with status: {job.status}")