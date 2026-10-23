from typing import List
from speech_client import get_assemblyai_client
from speech_models import TranscriptionResult, Word


def get_timestamped_transcript(job_id: str) -> TranscriptionResult:
    """
    Retrieves the timestamped words from a completed AssemblyAI transcription.
    """
    aai = get_assemblyai_client()
    transcriber = aai.Transcriber()
    transcript = transcriber.get_by_id(job_id)

    if transcript.status != "completed":
        # Assuming the job must be completed to get words.
        # A real implementation might poll here.
        return TranscriptionResult(id=transcript.id, status=transcript.status)

    words = []
    if transcript.words:
        for word in transcript.words:
            words.append(
                Word(
                    text=word.text,
                    start=word.start,
                    end=word.end,
                    confidence=word.confidence,
                )
            )

    return TranscriptionResult(id=transcript.id, status=transcript.status, words=words)
