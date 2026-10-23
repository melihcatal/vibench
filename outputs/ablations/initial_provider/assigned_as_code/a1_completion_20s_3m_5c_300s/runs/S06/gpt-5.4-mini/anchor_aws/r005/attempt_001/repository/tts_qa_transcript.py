import boto3


def tts_qa_transcript(payload, config=None):
    config = config or {}
    client = boto3.client("transcribe", region_name=config.get("region"))
    response = client.start_transcription_job(
        TranscriptionJobName=config.get("job_name", "tts-qa-transcript"),
        Media={"MediaFileUri": payload["media_uri"]},
        MediaFormat=config.get("media_format", "mp3"),
        LanguageCode=config.get("language_code", "en-US"),
        OutputBucketName=config.get("output_bucket"),
    )
    return {"job": response["TranscriptionJob"]}
