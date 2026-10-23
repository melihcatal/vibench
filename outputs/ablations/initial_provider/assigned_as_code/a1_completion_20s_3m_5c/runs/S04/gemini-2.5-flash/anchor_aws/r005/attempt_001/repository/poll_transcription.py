from speech_client import get_transcribe_client
from speech_models import normalize_transcription_job_status, parse_transcription_result, extract_transcript_text

def poll_transcription(job_id: str, config: dict = None):
    config = config or {}
    client = get_transcribe_client(region_name=config.get("region"))
    response = client.get_transcription_job(TranscriptionJobName=job_id)
    job = response["TranscriptionJob"]
    status = normalize_transcription_job_status(job["TranscriptionJobStatus"])
    result = {"job_id": job_id, "status": status}

    if status == "COMPLETED":
        transcript_uri = job["Transcript"]["TranscriptFileUri"]
        transcription_result = parse_transcription_result(transcript_uri)
        result["transcript"] = extract_transcript_text(transcription_result)
    elif status == "FAILED":
        result["error"] = job.get("FailureReason", "Transcription job failed")

    return result
