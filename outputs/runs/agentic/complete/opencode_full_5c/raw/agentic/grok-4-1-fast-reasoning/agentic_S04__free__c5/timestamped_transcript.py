import assemblyai as aai
from poll_transcription import poll_transcription
from typing import List, Dict, Any


def timestamped_transcript(job_id: str) -> List[Dict[str, Any]]:
    transcript = poll_transcription(job_id)
    return transcript["words"]
