import assemblyai as aai
from submit_transcription import submit_transcription
from poll_transcription import poll_transcription
from typing import List, Dict, Any


def diarized_transcript(audio_path: str) -> List[Dict[str, Any]]:
    job_id = submit_transcription(audio_path, diarize=True)
    transcript = poll_transcription(job_id)
    return transcript.get("utterances", [])
