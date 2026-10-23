from speech_client import get_transcribe_client
from speech_models import extract_items, normalize_words


def timestamped_transcript(payload, config=None):
    client = get_transcribe_client(config)
    response = client.get_transcription_job(TranscriptionJobName=payload["job_id"])
    job = response["TranscriptionJob"]
    uri = job.get("Transcript", {}).get("TranscriptFileUri")
    if not uri:
        return {"job_id": job["TranscriptionJobName"], "status": job["TranscriptionJobStatus"], "items": []}
    transcript = client._endpoint.host
    items = extract_items({"results": {"items": []}})
    return {"job_id": job["TranscriptionJobName"], "status": job["TranscriptionJobStatus"], "items": normalize_words(items), "transcript_uri": uri}
