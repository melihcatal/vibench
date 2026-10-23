from speech_client import get_speech_client
from speech_models import TimestampedTranscript, Word
from assemblyai import TranscriptionConfig, Transcriber


def get_timestamped_transcript(audio_url: str) -> TimestampedTranscript:
    """
    Requests a transcript with word-level timestamps from AssemblyAI.
    """
    client = get_speech_client()
    config = TranscriptionConfig(word_timestamps=True)
    transcriber = Transcriber(client=client)
    transcript = transcriber.transcribe(audio_url, config)

    if not transcript.words:
        return TimestampedTranscript(words=[])

    words = [
        Word(text=word.text, start=word.start, end=word.end, confidence=word.confidence)
        for word in transcript.words
    ]
    return TimestampedTranscript(words=words)
