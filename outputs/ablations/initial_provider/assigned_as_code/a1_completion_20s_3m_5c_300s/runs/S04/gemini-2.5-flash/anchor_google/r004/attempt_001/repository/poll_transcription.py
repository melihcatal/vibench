from google.cloud import speech
from speech_client import get_speech_client
from speech_models import TranscriptionResult

def poll_transcription(job_id):
    client = get_speech_client()
    operation = client.get_operation(name=job_id)

    if operation.done:
        response = operation.result()
        transcript = " ".join([result.alternatives[0].transcript for result in response.results])
        return TranscriptionResult(transcript=transcript)
    else:
        return {"status": "IN_PROGRESS"}
