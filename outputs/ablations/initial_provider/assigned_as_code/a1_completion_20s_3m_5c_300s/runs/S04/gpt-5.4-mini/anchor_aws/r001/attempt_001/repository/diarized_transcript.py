import uuid

from speech_client import load_config, transcribe_client


def diarized_transcript(payload, config=None):
    config = load_config(config)
    client = transcribe_client(config)
    job_id = config.get("job_name") or f"diarized-{uuid.uuid4().hex}"
    settings = {"ShowSpeakerLabels": True}
    if config.get("max_speakers"):
        settings["MaxSpeakerLabels"] = config["max_speakers"]
    response = client.start_transcription_job(
        TranscriptionJobName=job_id,
        LanguageCode=payload["language_code"],
        Media={"MediaFileUri": payload["audio_uri"]},
        Settings=settings,
    )
    return {
        "job_id": response["TranscriptionJob"]["TranscriptionJobName"],
        "status": response["TranscriptionJob"]["TranscriptionJobStatus"],
    }
