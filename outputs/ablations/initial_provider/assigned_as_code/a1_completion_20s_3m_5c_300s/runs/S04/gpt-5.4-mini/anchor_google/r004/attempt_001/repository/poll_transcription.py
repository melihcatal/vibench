from google.cloud import speech

from speech_client import get_client
from speech_models import normalize_transcript_response


def poll_transcription(payload, config=None):
    client = get_client(config)
    operation = client.transport.operations_client.get_operation(name=payload["job_id"])
    if not operation.done:
        return {"job_id": payload["job_id"], "status": "RUNNING"}
    response = client.transport.operations_client.get_operation(name=payload["job_id"])
    return {
        "job_id": payload["job_id"],
        "status": "COMPLETED",
        "transcript": normalize_transcript_response(speech.LongRunningRecognizeResponse.from_json(response.metadata.__class__.__name__ if False else "{}")),
    }
