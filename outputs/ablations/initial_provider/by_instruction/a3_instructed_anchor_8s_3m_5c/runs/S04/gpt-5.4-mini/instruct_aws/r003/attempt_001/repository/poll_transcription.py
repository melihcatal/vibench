from speech_client import transcribe_client
from speech_models import parse_transcript_payload


def poll_transcription(job_name: str) -> dict:
    client = transcribe_client()
    payload = client.get_transcription_job(TranscriptionJobName=job_name)
    return parse_transcript_payload(payload).__dict__
