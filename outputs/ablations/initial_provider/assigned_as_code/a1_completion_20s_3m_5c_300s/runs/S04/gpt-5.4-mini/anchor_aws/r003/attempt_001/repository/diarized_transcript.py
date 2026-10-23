import boto3


def diarized_transcript(payload, config=None):
    config = config or {}
    client = boto3.client("transcribe", region_name=config.get("region"))
    job_name = config.get("job_name") or payload["job_id"]
    response = client.start_transcription_job(
        TranscriptionJobName=job_name,
        LanguageCode=payload["language_code"],
        Media={"MediaFileUri": payload["audio_uri"]},
        Settings={"ShowSpeakerLabels": True, "MaxSpeakerLabels": payload.get("max_speakers", 2)},
    )
    return {
        "job_id": response["TranscriptionJob"]["TranscriptionJobName"],
        "status": response["TranscriptionJob"]["TranscriptionJobStatus"],
    }
