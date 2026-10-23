import boto3

from speech_client import load_config, s3_uri_from_path


def diarized_transcript(audio_path: str, job_name: str | None = None, max_speakers: int = 2) -> dict:
    config = load_config()
    client = boto3.client("transcribe", region_name=config.region)
    response = client.start_transcription_job(
        TranscriptionJobName=job_name or "diarized-transcription",
        Media={"MediaFileUri": s3_uri_from_path(audio_path)},
        MediaFormat="mp3",
        LanguageCode=config.language_code,
        Settings={"ShowSpeakerLabels": True, "MaxSpeakerLabels": max_speakers},
    )
    return response
