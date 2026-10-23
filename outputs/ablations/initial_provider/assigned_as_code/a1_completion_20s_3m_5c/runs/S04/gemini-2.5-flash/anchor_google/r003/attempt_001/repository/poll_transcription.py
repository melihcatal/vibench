from google.cloud import speech

def poll_transcription(job_id):
    client = speech.SpeechClient()
    operation = client.get_operation(job_id)

    if operation.done():
        response = operation.result()
        transcript = ""
        for result in response.results:
            transcript += result.alternatives[0].transcript + " "
        return {
            "status": "COMPLETED",
            "transcript": transcript.strip(),
        }
    else:
        return {
            "status": "IN_PROGRESS",
            "transcript": None,
        }
