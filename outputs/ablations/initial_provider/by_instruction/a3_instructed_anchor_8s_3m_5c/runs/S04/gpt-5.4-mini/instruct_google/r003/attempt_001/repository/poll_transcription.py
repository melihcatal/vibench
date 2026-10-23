from typing import Any, Dict

from google.cloud import speech_v1p1beta1 as speech

from speech_models import normalize_segments, normalize_text


def poll_transcription(job_name: str) -> Dict[str, Any]:
    client = speech.SpeechClient()
    operation = client.transport.operations_client.get_operation(name=job_name)
    if not operation.done:
        return {"job_name": job_name, "done": False, "transcript": "", "segments": []}
    result = client.transport.operations_client._get_operation(name=job_name)
    response = result.response
    transcript = normalize_text(response)
    segments = normalize_segments(response)
    return {"job_name": job_name, "done": True, "transcript": transcript, "segments": segments, "raw": response}
