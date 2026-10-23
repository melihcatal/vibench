from speech_client import get_assemblyai_client
from speech_models import TranscriptionRequest


def submit_transcription_job(audio_url: str):
    client = get_assemblyai_client()
    config = client.TranscriptionConfig(speaker_diarization=False, word_boost=[])
    transcript = client.transcribe(audio_url, config)
    return {"id": transcript.id, "status": transcript.status}
