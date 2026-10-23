import uuid

from speech_client import get_transcribe_client

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
        }
    )
    return {
        "job_id": response["TranscriptionJob"]["TranscriptionJobName"],
        "status": "SUBMITTED",
    }
