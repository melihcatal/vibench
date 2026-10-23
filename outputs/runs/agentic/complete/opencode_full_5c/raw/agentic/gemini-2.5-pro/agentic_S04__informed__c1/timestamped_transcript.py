from speech_client import get_speech_client
from speech_models import TimestampedWord


def get_timestamped_transcript(job_id: str) -> list[TimestampedWord]:
    """
    Returns word timestamps from an AssemblyAI transcription result.
    """
    client = get_speech_client()
    transcript = client.transcripts.get(transcript_id=job_id)

    if transcript.status != "completed":
        return []

    words = []
    if transcript.words:
        for word in transcript.words:
            words.append(
                TimestampedWord(text=word.text, start=word.start, end=word.end)
            )
    return words
