import boto3

from speech_client import load_config


def tts_qa_transcript(payload, config=None):
    cfg = load_config(config)
    client = boto3.client("transcribe", region_name=cfg.region)
    job_name = payload["job_name"]
    media_uri = payload["media_uri"]
    language_code = payload.get("language_code", "en-US")
    client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": media_uri},
        MediaFormat=payload.get("media_format", "mp3"),
        LanguageCode=language_code,
    )
    result = client.get_transcription_job(TranscriptionJobName=job_name)
    job = result["TranscriptionJob"]
    transcript_uri = job.get("Transcript", {}).get("TranscriptFileUri")
    return {"job_status": job.get("TranscriptionJobStatus"), "transcript_uri": transcript_uri}
