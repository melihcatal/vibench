from __future__ import annotations

from speech_client import assemblyai_post
from speech_models import BatchTranscriptionRequest, normalize_assemblyai_transcript, transcript_segments_from_utterances


def diarized_transcript(audio_url: str, language_code: str | None = None) -> dict:
    request = BatchTranscriptionRequest(
        audio_url=audio_url,
        language_code=language_code,
        speaker_labels=True,
        punctuate=True,
        format_text=True,
    )
    response = assemblyai_post("/transcript", request.to_assemblyai_payload())
    transcript = normalize_assemblyai_transcript(response)
    segments = transcript_segments_from_utterances(transcript.utterances)
    return {
        "provider": "AssemblyAI",
        "transcript_id": transcript.transcript_id,
        "status": transcript.status,
        "segments": [segment.__dict__ for segment in segments],
    }
