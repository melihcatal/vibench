from google.cloud import speech


def poll_transcription(payload, config=None):
    config = config or {}
    client = speech.SpeechClient()
    operation = client.get_operation(payload["job_id"])
    if not operation.done:
        return {"job_id": payload["job_id"], "status": "PENDING"}
    result = operation.result()
    transcripts = []
    for res in result.results:
        transcripts.append(res.alternatives[0].transcript)
    return {"job_id": payload["job_id"], "status": "COMPLETED", "transcript": "\n".join(transcripts)}
