from google.cloud import speech

from speech_client import get_speech_client


def poll_transcription(job_id):
    client = get_speech_client()
    operation = client.get_operation(name=job_id)
    if operation.done:
        response = operation.result()
        transcript = response.results[0].alternatives[0].transcript
        return {
            "transcript": transcript,
            "status": "COMPLETED"
        }
    else:
        return {
            "status": "PENDING"
        }