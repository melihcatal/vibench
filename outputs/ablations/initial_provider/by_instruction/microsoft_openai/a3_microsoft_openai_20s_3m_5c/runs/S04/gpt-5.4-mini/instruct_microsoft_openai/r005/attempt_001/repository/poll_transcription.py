from speech_client import OpenAIHttpClient
from speech_models import normalize_transcript_text


def poll_transcription(job_id: str) -> str:
    client = OpenAIHttpClient()
    response = client.get(f"/audio/transcriptions/{job_id}")
    response.raise_for_status()
    return normalize_transcript_text(response.json())
