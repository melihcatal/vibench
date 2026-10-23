from google.cloud import speech

def poll_transcription(job_id):
    client = speech.SpeechClient()
    operation = client.get_operation(name=job_id)
    if operation.done:
        response = operation.result()
        return {
            "status": "COMPLETED",
            "transcript": response.results[0].alternatives[0].transcript,
        }
    else:
        return {"status": "IN_PROGRESS"}