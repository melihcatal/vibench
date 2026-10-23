from google.cloud import speech

from speech_client import get_speech_client


def get_timestamps(job_id):
    client = get_speech_client()
    operation = client.get_operation(name=job_id)
    if operation.done:
        response = operation.result()
        timestamps = response.results[0].alternatives[0].words
        return {
            "timestamps": timestamps,
            "status": "COMPLETED"
        }
    else:
        return {
            "status": "PENDING"
        }