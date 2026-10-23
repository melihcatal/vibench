from google.cloud import speech

def poll_transcription(job_id):
    client = speech.SpeechClient()
    operation = client.get_operation(name=job_id)
    if operation.done:
        response = operation.result()
        return normalize_transcription_response(response)
    else:
        return {'status': 'IN_PROGRESS'}