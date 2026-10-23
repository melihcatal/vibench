from speech_client import speech_get
from speech_models import extract_timestamps


def timestamped_transcript(job_id, config=None):
    payload = speech_get(f"/transcriptions/{job_id}/files", config=config)
    files = payload.get('values', payload.get('files', []))
    if not files:
        return {'job_id': job_id, 'timestamps': []}
    return {'job_id': job_id, 'timestamps': extract_timestamps(files[0])}
