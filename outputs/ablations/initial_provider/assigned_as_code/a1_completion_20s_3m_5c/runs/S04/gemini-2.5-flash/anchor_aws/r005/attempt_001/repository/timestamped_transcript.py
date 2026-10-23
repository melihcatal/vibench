import uuid

from speech_client import get_transcribe_client
from speech_models import normalize_transcription_job_status, parse_transcription_result, extract_timestamped_words, extract_segment_timestamps

def timestamped_transcript(payload: dict, config: dict = None):
    config = config or {}
    client = get_transcribe_client(region_name=config.get("region"))
    job_id = config.get("job_name") or f"timestamped-{uuid.uuid4().hex}"
    response = client.start_transcription_job(
        TranscriptionJobName=job_id,
        LanguageCode=payload["language_code"],
        Media={"MediaFileUri": payload["audio_uri"]},
        Settings={
            "ShowSpeakerLabels": False, # Not relevant for word timestamps primarily
            "ShowAlternatives": False, # Not relevant for word timestamps primarily
            "WordStability": "LOW", # Default value, can be adjusted
        }
    )

    job = response["TranscriptionJob"]
    status = normalize_transcription_job_status(job["TranscriptionJobStatus"])
    result = {"job_id": job_id, "status": status}

    if status == "COMPLETED":
        transcript_uri = job["Transcript"]["TranscriptFileUri"]
        transcription_result = parse_transcription_result(transcript_uri)
        
        if payload.get("segment_timestamps", False):
            result["segments"] = extract_segment_timestamps(transcription_result)
        else:
            result["words"] = extract_timestamped_words(transcription_result)

    elif status == "FAILED":
        result["error"] = job.get("FailureReason", "Transcription job failed")

    return result
