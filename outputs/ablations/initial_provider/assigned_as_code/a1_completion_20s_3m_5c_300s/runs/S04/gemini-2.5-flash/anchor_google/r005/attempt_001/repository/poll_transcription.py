from google.cloud import speech
from speech_client import get_speech_client
from speech_models import TranscriptionJob

def poll_transcription(job_id: str) -> TranscriptionJob:
    client = get_speech_client()
    operation = client.get_operation(name=job_id)

    if operation.done:
        response = operation.result()
        transcript = " ".join([result.alternatives[0].transcript for result in response.results])
        return TranscriptionJob(
            job_id=job_id,
            status="COMPLETED",
            transcript=transcript,
        )
    else:
        return TranscriptionJob(job_id=job_id, status="IN_PROGRESS")
