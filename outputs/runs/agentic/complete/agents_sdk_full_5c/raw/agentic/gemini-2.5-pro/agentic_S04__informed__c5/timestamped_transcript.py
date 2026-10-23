from typing import List
from speech_client import get_speech_client
from speech_models import TimestampedWord


def get_timestamped_transcript(audio_url: str) -> List[TimestampedWord]:
    """
    Transcribes an audio file and returns word-level timestamps.

    Args:
        audio_url: The public URL of the audio file.

    Returns:
        A list of words with their start and end timestamps.
    """
    aai = get_speech_client()
    transcriber = aai.Transcriber()

    # No specific config needed for word timestamps, it's default
    transcript = transcriber.transcribe(audio_url)

    if transcript.status == "error":
        raise RuntimeError(f"Transcription failed: {transcript.error}")

    if not transcript.words:
        return []

    return [
        TimestampedWord(
            start=word.start,
            end=word.end,
            text=word.text,
            confidence=word.confidence
        )
        for word in transcript.words
    ]
