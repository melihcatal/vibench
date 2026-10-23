from assemblyai import Transcriber

from speech_models import normalize_transcript


def poll_transcription(transcript_id: str):
    transcriber = Transcriber()
    transcript = transcriber.get(transcript_id)
    return normalize_transcript(transcript)
