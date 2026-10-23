import boto3

from speech_client import get_transcribe_client, load_speech_config


def timestamped_transcript(payload, config=None):
    cfg = load_speech_config(config)
    client = get_transcribe_client(cfg)
    response = client.start_transcription_job(
        TranscriptionJobName=payload.get("job_name") or cfg["job_name"],
        LanguageCode=payload["language_code"],
        Media={"MediaFileUri": payload["audio_uri"]},
        Settings={"ShowAlternatives": False},
        OutputBucketName=cfg["output_bucket"],
        Subtitles={"Formats": ["srt", "vtt"], "OutputStartIndex": 1},
    )
    return {"job_id": response["TranscriptionJob"]["TranscriptionJobName"], "status": "SUBMITTED"}
