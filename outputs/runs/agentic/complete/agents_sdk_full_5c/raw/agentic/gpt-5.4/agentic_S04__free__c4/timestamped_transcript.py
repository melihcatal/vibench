from __future__ import annotations

from speech_client import assemblyai_get
from speech_models import normalize_assemblyai_transcript, transcript_segments_from_utterances, transcript_segments_from_words


def timestamped_transcript(transcript_id: str, granularity: str = "word") -> dict:
    response = assemblyai_get(f"/transcript/{transcript_id}")
    transcript = normalize_assemblyai_transcript(response)
    if granularity == "segment":
        segments = transcript_segments_from_utterances(transcript.utterances)
    else:
        segments = transcript_segments_from_words(transcript.words)
    return {
        "provider": "AssemblyAI",
        "transcript_id": transcript.transcript_id,
        "status": transcript.status,
        "granularity": granularity,
        "timestamps": [segment.__dict__ for segment in segments],
    }
