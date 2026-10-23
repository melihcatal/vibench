from speech_client import get_speech_client
from speech_models import normalize_transcript_result

def poll_transcription(job_id: str):
    client = get_speech_client()
    operation = client.get_operation(name=job_id)

    if operation.done:
        return normalize_transcript_result(job_id, operation.to_dict())
    else:
        return {
            "job_id": job_id,
            "status": "IN_PROGRESS",
        }
