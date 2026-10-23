import boto3

from speech_client import load_config


def timestamped_transcript(job_name: str) -> dict:
    config = load_config()
    client = boto3.client("transcribe", region_name=config.region)
    response = client.get_transcription_job(TranscriptionJobName=job_name)
    transcript_uri = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
    import urllib.request
    with urllib.request.urlopen(transcript_uri) as handle:
        data = __import__("json").load(handle)
    return {"items": data.get("results", {}).get("items", []), "segments": data.get("results", {}).get("speaker_labels", {}).get("segments", []), "raw": data}
