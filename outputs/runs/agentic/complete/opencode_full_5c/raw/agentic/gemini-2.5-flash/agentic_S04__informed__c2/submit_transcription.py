import assemblyai
from speech_client import get_assemblyai_client
from speech_models import TranscriptionRequest


def submit_transcription(audio_url: str, diarization: bool = False) -> str:
    client = get_assemblyai_client()
    config = assemblyai.TranscriptionConfig(speaker_diarization=diarization)
    transcript = client.transcripts.submit(audio_url=audio_url, config=config)
    return transcript.id
