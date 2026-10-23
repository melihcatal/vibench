import assemblyai as aai
from speech_client import require_api_key
from speech_models import normalize_transcript_payload


def timestamped_transcript(transcript_id: str) -> dict:
    aai.settings.api_key = require_api_key()
    transcript = aai.Transcript.get(transcript_id)
    data = normalize_transcript_payload(transcript.json_response)
    return {"id": data["id"], "words": data["words"], "segments": data["segments"]}
