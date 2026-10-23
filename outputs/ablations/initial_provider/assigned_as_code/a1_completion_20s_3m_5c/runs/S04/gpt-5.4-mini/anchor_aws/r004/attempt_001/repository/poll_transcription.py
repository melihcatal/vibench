import boto3

from speech_client import get_transcribe_client, load_speech_config
from speech_models import TranscriptResponse, normalize_segments


def poll_transcription(payload, config=None):
    cfg = load_speech_config(config)
    client = get_transcribe_client(cfg)
    response = client.get_transcription_job(TranscriptionJobName=payload["job_id"])
    job = response["TranscriptionJob"]
    transcript = ""
    segments = []
    if job.get("Transcript", {}).get("TranscriptFileUri"):
        transcript = job["Transcript"]["TranscriptFileUri"]
    if job.get("Subtitles"):
        segments = normalize_segments(job.get("Subtitles", {}).get("Formats", []))
    return TranscriptResponse(
        job_id=job["TranscriptionJobName"],
        status=job["TranscriptionJobStatus"],
        transcript=transcript,
        segments=segments,
    ).__dict__
