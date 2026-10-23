import assemblyai as aai
from speech_client import require_api_key
from speech_models import normalize_transcript_payload


def diarized_transcript(audio_file: str) -> dict:
    aai.settings.api_key = require_api_key()
    transcriber = aai.Transcriber(config=aai.TranscriptionConfig(speaker_labels=True))
    transcript = transcriber.transcribe(audio_file)
    return normalize_transcript_payload(transcript.json_response)
