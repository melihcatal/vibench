from assemblyai import Transcriber

from speech_models import normalize_transcript


def timestamped_transcript(audio_url: str):
    transcriber = Transcriber()
    transcript = transcriber.transcribe(audio_url, config={"word_timestamps": True})
    return normalize_transcript(transcript)
