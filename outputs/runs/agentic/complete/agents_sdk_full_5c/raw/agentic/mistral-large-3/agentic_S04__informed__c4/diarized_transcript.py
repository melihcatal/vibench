from typing import List, Dict
from speech_client import get_assemblyai_client
from speech_models import SpeakerLabel


def diarized_transcript(job_id: str) -> List[SpeakerLabel]:
    """
    Retrieve speaker diarization results from an AssemblyAI transcription job.
    Returns a list of speaker-labeled segments with text and timestamps.
    """
    client = get_assemblyai_client()
    transcript = client.transcripts.get(job_id)
    if not transcript.utterances:
        raise ValueError(f"No speaker diarization found for job {job_id}")
    
    return [
        SpeakerLabel(
            speaker=utterance.speaker,
            text=utterance.text,
            start=utterance.start,
            end=utterance.end
        )
        for utterance in transcript.utterances
    ]