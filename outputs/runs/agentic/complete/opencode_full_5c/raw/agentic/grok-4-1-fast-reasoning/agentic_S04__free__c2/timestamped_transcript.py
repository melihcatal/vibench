import assemblyai as aai
from speech_client import get_client
from speech_models import serialize_transcript
from typing import List, Dict, Any


def timestamped_transcript(job_id: str) -> List[Dict[str, Any]]:
    client = get_client()
    transcript = client.transcripts.get(job_id)
    if transcript.status != aai.TranscriptStatus.completed:
        raise ValueError("Transcription job not completed")
    serialized = serialize_transcript(transcript)
    return serialized["words"]
