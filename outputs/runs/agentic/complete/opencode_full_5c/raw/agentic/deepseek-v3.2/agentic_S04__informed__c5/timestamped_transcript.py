import assemblyai as aai
from speech_client import get_speech_client


def timestamped_transcript(transcript_id: str) -> dict:
    """Return word or segment timestamps from a transcription result."""
    client = get_speech_client()

    transcript = client.transcript.get(transcript_id)

    if transcript.status != aai.TranscriptStatus.completed:
        raise Exception(f"Transcript not completed: {transcript.status}")

    word_timestamps = []
    if transcript.words:
        for word in transcript.words:
            word_timestamps.append(
                {
                    "text": word.text,
                    "start": word.start,
                    "end": word.end,
                    "confidence": word.confidence,
                }
            )

    segment_timestamps = []
    if transcript.utterances:
        for segment in transcript.utterances:
            segment_timestamps.append(
                {
                    "text": segment.text,
                    "start": segment.start,
                    "end": segment.end,
                    "speaker": segment.speaker if hasattr(segment, "speaker") else None,
                }
            )

    return {
        "word_timestamps": word_timestamps,
        "segment_timestamps": segment_timestamps,
        "full_text": transcript.text,
    }
