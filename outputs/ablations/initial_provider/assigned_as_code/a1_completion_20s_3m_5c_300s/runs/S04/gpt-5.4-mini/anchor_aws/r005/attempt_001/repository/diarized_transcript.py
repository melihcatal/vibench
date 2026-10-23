import uuid

from speech_client import get_transcribe_client, normalize_media_uri
from speech_models import normalize_segments


def diarized_transcript(payload, config=None):
    client = get_transcribe_client(config)
    job_id = payload.get("job_name") or f"diarized-{uuid.uuid4().hex}"
    response = client.start_transcription_job(
        TranscriptionJobName=job_id,
        LanguageCode=payload["language_code"],
        Media={"MediaFileUri": normalize_media_uri(payload, config)},
        Settings={"ShowSpeakerLabels": True, "MaxSpeakerLabels": payload.get("max_speakers", 2)},
    )
    job = response["TranscriptionJob"]
    return {"job_id": job["TranscriptionJobName"], "status": job["TranscriptionJobStatus"], "segments": normalize_segments([])}
