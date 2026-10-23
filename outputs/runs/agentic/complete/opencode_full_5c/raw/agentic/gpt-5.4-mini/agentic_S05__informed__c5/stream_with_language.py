from typing import Iterator

from google.cloud import speech

from speech_client import build_streaming_config, create_client
from speech_models import TranscriptEvent, TranscriptionRequest


def stream_with_language(
    audio_content: Iterator[bytes], language_code: str, enable_punctuation: bool = True
) -> Iterator[TranscriptEvent]:
    client = create_client()
    config = build_streaming_config(
        TranscriptionRequest(
            language_code=language_code, enable_punctuation=enable_punctuation
        )
    )
    requests = (
        speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in audio_content
    )
    for response in client.streaming_recognize(config, requests):
        for result in response.results:
            if result.alternatives:
                yield TranscriptEvent(
                    text=result.alternatives[0].transcript,
                    is_final=result.is_final,
                    language=language_code,
                )
