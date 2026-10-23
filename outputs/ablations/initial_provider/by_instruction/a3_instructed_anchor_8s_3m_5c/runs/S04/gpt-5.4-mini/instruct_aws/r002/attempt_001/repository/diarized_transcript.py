import boto3

from speech_client import load_config, normalize_uri


def diarized_transcript(media_uri: str, job_name: str, language_code: str = "en-US") -> dict:
    config = load_config()
    client = boto3.client(
        "transcribe",
        region_name=config.aws_region,
        aws_access_key_id=config.aws_access_key_id,
        aws_secret_access_key=config.aws_secret_access_key,
        aws_session_token=config.aws_session_token,
    )
    return client.start_transcription_job(
        TranscriptionJobName=job_name,
        LanguageCode=language_code,
        Media={"MediaFileUri": normalize_uri(media_uri)},
        Settings={"ShowSpeakerLabels": True, "MaxSpeakerLabels": 10},
    )
