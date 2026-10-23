from speech_client import build_client
from speech_models import normalize_text


def poll_transcription(job_id: str):
    client = build_client()
    result = client.audio.transcriptions.retrieve(job_id)
    transcript = getattr(result, "text", None) or normalize_text(result)
    return {
        "job_id": job_id,
        "status": getattr(result, "status", None),
        "transcript": transcript,
        "raw": result,
    }
