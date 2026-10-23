import assemblyai as aai
from speech_client import require_api_key
from speech_models import normalize_transcript_payload


def poll_transcription(transcript_id: str) -> dict:
    aai.settings.api_key = require_api_key()
    transcript = aai.Transcript.get(transcript_id)
    return normalize_transcript_payload(transcript.json_response)
