import uuid

from speech_client import get_transcribe_client
from speech_models import normalize_transcription_job_status, parse_transcription_result, extract_diarization_segments

def diarized_transcript(payload: dict, config: dict = None):
    config = config or {}
    client = get_transcribe_client(region_name=config.get("region"))
    job_id = config.get("job_name") or f"diarization-{uuid.uuid4().hex}"
    response = client.start_transcription_job(
        TranscriptionJobName=job_id,
        LanguageCode=payload["language_code"],
        Media={"MediaFileUri": payload["audio_uri"]},
        Settings={
            "ShowSpeakerLabels": True,
            "MaxSpeakerLabels": payload.get("max_speaker_labels", 2)
        },
        ContentRedaction=payload.get("content_redaction"),
        PiiEntityTypes=payload.get("pii_entity_types"),
    )
    
    job = response["TranscriptionJob"]
    status = normalize_transcription_job_status(job["TranscriptionJobStatus"])
    result = {"job_id": job_id, "status": status}

    if status == "COMPLETED":
        transcript_uri = job["Transcript"]["TranscriptFileUri"]
        transcription_result = parse_transcription_result(transcript_uri)
        result["diarized_segments"] = extract_diarization_segments(transcription_result)
    elif status == "FAILED":
        result["error"] = job.get("FailureReason", "Transcription job failed")

    return result
