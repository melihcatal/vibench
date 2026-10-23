import boto3

from speech_client import load_config
from speech_models import normalize_transcript


def poll_transcription(job_name: str) -> dict:
    config = load_config()
    client = boto3.client("transcribe", region_name=config.region)
    response = client.get_transcription_job(TranscriptionJobName=job_name)
    job = response["TranscriptionJob"]
    if job["TranscriptionJobStatus"] != "COMPLETED":
        return {"status": job["TranscriptionJobStatus"], "raw": response}
    transcript_uri = job["Transcript"]["TranscriptFileUri"]
    import urllib.request
    with urllib.request.urlopen(transcript_uri) as handle:
        data = __import__("json").load(handle)
    return normalize_transcript(data)
