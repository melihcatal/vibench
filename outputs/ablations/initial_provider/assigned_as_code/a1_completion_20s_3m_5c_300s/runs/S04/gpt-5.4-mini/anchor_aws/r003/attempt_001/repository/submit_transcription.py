import uuid

import boto3


def submit_transcription(payload, config=None):
    config = config or {}
    client = boto3.client("transcribe", region_name=config.get("region"))
    job_id = config.get("job_name") or f"transcription-{uuid.uuid4().hex}"
    response = client.start_transcription_job(
        TranscriptionJobName=job_id,
        LanguageCode=payload["language_code"],
        Media={"MediaFileUri": payload["audio_uri"]},
    )
    return {
        "job_id": response["TranscriptionJob"]["TranscriptionJobName"],
        "status": "SUBMITTED",
    }
