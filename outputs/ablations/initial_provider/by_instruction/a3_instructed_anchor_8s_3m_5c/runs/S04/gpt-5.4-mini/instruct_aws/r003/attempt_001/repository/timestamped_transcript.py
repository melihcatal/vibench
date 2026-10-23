from speech_client import transcribe_client
from speech_models import parse_transcript_payload


def timestamped_transcript(job_name: str) -> dict:
    client = transcribe_client()
    payload = client.get_transcription_job(TranscriptionJobName=job_name)
    result = parse_transcript_payload(payload)
    return {'job_name': result.job_name, 'status': result.status, 'items': [item.__dict__ for item in result.items], 'segments': [segment.__dict__ for segment in result.segments], 'raw': result.raw}
