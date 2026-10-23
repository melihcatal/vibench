import os
import assemblyai as aai
from speech_client import require_api_key
from speech_models import TranscriptRequest, normalize_transcript_payload


def submit_transcription(audio_file: str) -> dict:
    aai.settings.api_key = require_api_key()
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)
    return normalize_transcript_payload(transcript.json_response)
