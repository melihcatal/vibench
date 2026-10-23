from speech_client import get_transcribe_client
from speech_models import extract_transcript_text


def poll_transcription(payload, config=None):
    client = get_transcribe_client(config)
    response = client.get_transcription_job(TranscriptionJobName=payload["job_id"])
    job = response["TranscriptionJob"]
    result = {"job_id": job["TranscriptionJobName"], "status": job["TranscriptionJobStatus"]}
    if job["TranscriptionJobStatus"] == "COMPLETED":
        result["transcript"] = extract_transcript_text(job)
        result["transcript_uri"] = job.get("Transcript", {}).get("TranscriptFileUri")
    return result
