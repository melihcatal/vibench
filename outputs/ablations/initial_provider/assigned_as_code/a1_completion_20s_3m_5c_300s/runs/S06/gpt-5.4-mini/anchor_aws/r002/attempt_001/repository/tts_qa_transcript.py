from speech_client import load_config

import boto3


def tts_qa_transcript(payload, config=None):
    cfg = load_config(config)
    client = boto3.client("transcribe", region_name=cfg["region"])
    response = client.start_transcription_job(TranscriptionJobName=payload["job_name"], Media={"MediaFileUri": payload["media_uri"]}, MediaFormat=payload.get("media_format", "mp3"), LanguageCode=payload.get("language_code", "en-US"))
    return {"job": response["TranscriptionJob"], "job_name": payload["job_name"]}
