import boto3

from speech_client import get_transcribe_client, load_speech_config


def diarized_transcript(payload, config=None):
    cfg = load_speech_config(config)
    client = get_transcribe_client(cfg)
    job_name = cfg["job_name"] or payload.get("job_name")
    response = client.start_transcription_job(
        TranscriptionJobName=job_name,
        LanguageCode=payload["language_code"],
        Media={"MediaFileUri": payload["audio_uri"]},
        Settings={"ShowSpeakerLabels": True, "MaxSpeakerLabels": payload.get("max_speakers", 2)},
    )
    return {"job_id": response["TranscriptionJob"]["TranscriptionJobName"], "status": "SUBMITTED"}
