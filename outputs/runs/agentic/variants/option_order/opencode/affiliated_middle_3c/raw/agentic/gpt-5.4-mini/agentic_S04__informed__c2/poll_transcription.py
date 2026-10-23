from speech_client import create_transcriber
from speech_models import normalize_assemblyai_transcript


def poll_transcription(transcription_id: str):
    transcriber = create_transcriber()
    transcript = transcriber.get_transcript(transcription_id)
    return normalize_assemblyai_transcript(transcript.__dict__)
