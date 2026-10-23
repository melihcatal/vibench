from google.cloud import speech
from speech_client import get_speech_client


def poll_transcription(job_id):
    client = get_speech_client()
    operation = client.get_operation(name=job_id)
    if operation.done:
        response = client.get_operation(name=job_id).result()
        return normalize_transcription_response(response)
    return {"status": "IN_PROGRESS"}