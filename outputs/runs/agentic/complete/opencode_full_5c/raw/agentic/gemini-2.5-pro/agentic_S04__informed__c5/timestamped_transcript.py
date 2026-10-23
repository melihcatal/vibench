from speech_client import get_speech_client
from speech_models import TimestampedTranscript, Word


def get_timestamped_transcript(audio_file_path: str) -> TimestampedTranscript:
    aai = get_speech_client()
    config = aai.TranscriptionConfig(word_details=True)
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file_path, config)

    if transcript.status == "error":
        return TimestampedTranscript(words=[])

    words = [
        Word(text=word.text, start=word.start, end=word.end, confidence=word.confidence)
        for word in transcript.words
    ]
    return TimestampedTranscript(words=words)
