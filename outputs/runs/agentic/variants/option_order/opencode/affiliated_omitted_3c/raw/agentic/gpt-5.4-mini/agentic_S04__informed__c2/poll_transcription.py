import os
import assemblyai as aai
from speech_client import load_speech_config
from speech_models import normalize_segments


def poll_transcription(transcript_id: str):
    cfg = load_speech_config()
    aai.settings.api_key = cfg.api_key or os.environ["ASSEMBLYAI_API_KEY"]
    transcript = aai.Transcript.get(transcript_id)
    payload = transcript.json_response
    return {"text": payload.get("text", ""), "segments": [s.__dict__ for s in normalize_segments(payload)]}
