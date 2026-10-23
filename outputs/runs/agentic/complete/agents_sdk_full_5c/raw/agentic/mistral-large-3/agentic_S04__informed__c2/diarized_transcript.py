from typing import List, Dict
from speech_client import get_assemblyai_client
from speech_models import DiarizedSegment

def diarized_transcript(job_id: str) -> List[DiarizedSegment]:
    """
    Retrieve speaker diarization results for a completed AssemblyAI transcription job.
    Returns a list of segments with speaker labels and text.
    """
    client = get_assemblyai_client()
    transcript = client.transcripts.get(job_id)
    if transcript.status != "completed":
        raise ValueError(f"Transcription job not completed. Status: {transcript.status}")

    utterances = transcript.utterances
    if not utterances:
        raise ValueError("No speaker diarization data available.")

    segments = []
    for utterance in utterances:
        segments.append(
            DiarizedSegment(
                speaker=f"Speaker {utterance.speaker}",
                text=utterance.text,
                start=utterance.start,
                end=utterance.end
            )
        )
    return segments