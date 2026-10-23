from assemblyai import Transcriber

from speech_models import normalize_transcript


def diarized_transcript(audio_url: str):
    transcriber = Transcriber()
    transcript = transcriber.transcribe(audio_url, config={"speaker_labels": True})
    return normalize_transcript(transcript)
