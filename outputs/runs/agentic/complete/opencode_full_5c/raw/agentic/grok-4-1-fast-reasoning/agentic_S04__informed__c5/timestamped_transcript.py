from speech_client import get_speech_client
from assemblyai import TranscriptStatus


def timestamped_transcript(job_id: str) -> list[dict]:
    client = get_speech_client()
    transcript = client.transcripts.retrieve(job_id)
    if transcript.status != TranscriptStatus.completed:
        raise ValueError("Transcription not completed")
    words = []
    if hasattr(transcript, "words") and transcript.words:
        for word in transcript.words:
            words.append(
                {
                    "word": word.word,
                    "start_ms": getattr(word, "start", None),
                    "end_ms": getattr(word, "end", None),
                    "confidence": getattr(word, "confidence", None),
                }
            )
    return words
