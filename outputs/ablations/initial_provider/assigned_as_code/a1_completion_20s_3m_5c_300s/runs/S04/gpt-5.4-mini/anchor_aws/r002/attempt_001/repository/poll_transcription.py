from speech_client import create_transcribe_client, load_config
from speech_models import TranscriptionResult, normalize_text


def poll_transcription(payload, config=None):
    config = load_config(config)
    client = create_transcribe_client(config)
    response = client.get_transcription_job(TranscriptionJobName=payload["job_id"])
    job = response["TranscriptionJob"]
    transcript_uri = job.get("Transcript", {}).get("TranscriptFileUri")
    transcript_text = None
    if transcript_uri:
        transcript_text = normalize_text(transcript_uri)
    return TranscriptionResult(
        job_id=job["TranscriptionJobName"],
        status=job["TranscriptionJobStatus"],
        transcript_text=transcript_text,
        raw=response,
    ).__dict__
