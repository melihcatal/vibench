from speech_client import speech_get
from speech_models import extract_transcript_text


def poll_transcription(job_id, config=None):
    payload = speech_get(f"/transcriptions/{job_id}", config=config)
    if payload.get('status') not in {'Succeeded', 'succeeded'}:
        return {'job_id': job_id, 'status': payload.get('status')}
    content = speech_get(f"/transcriptions/{job_id}/files", config=config)
    files = content.get('values', content.get('files', []))
    transcript = ''
    if files:
        transcript = extract_transcript_text(files[0])
    return {'job_id': job_id, 'status': payload.get('status'), 'transcript': transcript}
