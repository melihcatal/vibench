from google.cloud import speech

from speech_client import get_speech_client


def request_diarization(job_id):
    client = get_speech_client()
    operation = client.get_operation(name=job_id)
    if operation.done:
        response = operation.result()
        diarization_results = response.results[0].speaker_labels
        return {
            "diarization_results": diarization_results,
            "status": "COMPLETED"
        }
    else:
        return {
            "status": "PENDING"
        }