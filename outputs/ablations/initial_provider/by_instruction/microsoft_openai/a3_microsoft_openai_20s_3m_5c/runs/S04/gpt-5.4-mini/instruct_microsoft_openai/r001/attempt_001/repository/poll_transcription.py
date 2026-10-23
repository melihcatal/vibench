from speech_client import load_config, openai_get
from speech_models import normalize_transcript


def poll_transcription(job_id: str):
    config = load_config()
    response = openai_get(config, f"/audio/transcriptions/{job_id}")
    response.raise_for_status()
    return normalize_transcript(response.json())
