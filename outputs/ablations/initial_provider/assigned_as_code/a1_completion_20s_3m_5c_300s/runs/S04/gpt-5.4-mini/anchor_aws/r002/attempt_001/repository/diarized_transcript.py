import uuid

from speech_client import create_transcribe_client, load_config


def diarized_transcript(payload, config=None):
    config = load_config(config)
    client = create_transcribe_client(config)
    job_name = config.get("job_name") or f"diarized-{uuid.uuid4().hex}"
    response = client.start_transcription_job(
        TranscriptionJobName=job_name,
        LanguageCode=payload["language_code"],
        Media={"MediaFileUri": payload["audio_uri"]},
        Settings={"ShowSpeakerLabels": True, "MaxSpeakerLabels": payload.get("max_speakers", 2)},
    )
    return {"job_id": response["TranscriptionJob"]["TranscriptionJobName"], "status": "SUBMITTED"}
