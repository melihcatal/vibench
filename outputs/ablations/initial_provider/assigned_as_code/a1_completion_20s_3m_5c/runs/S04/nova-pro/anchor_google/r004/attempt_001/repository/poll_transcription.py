from google.cloud import speech



def poll_transcription(job_id):
    client = speech.SpeechClient()
    operation = client.get_operation(name=job_id)
    if operation.done:
        response = operation.result()
        transcript = response.results[-1].alternatives[0].transcript
        return {"transcript": transcript, "status": "COMPLETED"}
    else:
        return {"status": "IN_PROGRESS"}