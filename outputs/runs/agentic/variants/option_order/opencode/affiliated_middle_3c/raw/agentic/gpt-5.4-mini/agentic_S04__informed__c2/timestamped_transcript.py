from speech_client import create_transcriber
from speech_models import extract_segments


def timestamped_transcript(transcription_id: str):
    transcriber = create_transcriber()
    transcript = transcriber.get_transcript(transcription_id)
    payload = transcript.__dict__
    return {
        "id": payload.get("id", transcription_id),
        "segments": extract_segments(payload),
        "raw": payload,
    }
