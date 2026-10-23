from google.cloud import speech

from speech_models import normalize_segments, normalize_transcript


def poll_transcription(payload, config=None):
    client = speech.SpeechClient()
    operation = client.transport.operations_client.get_operation(name=payload["job_id"])
    if not operation.done:
        return {"job_id": payload["job_id"], "status": "PENDING"}
    result = client.get_operation(name=payload["job_id"]).result()
    transcripts = []
    for response in getattr(result, "results", []):
        if getattr(response, "alternatives", None):
            transcripts.append(response.alternatives[0].transcript)
    return {
        "job_id": payload["job_id"],
        "status": "COMPLETED",
        "transcript": normalize_transcript(transcripts),
        "segments": normalize_segments(getattr(result, "results", [])),
    }
