from typing import Iterator

from google.cloud import speech_v1 as speech

from speech_client import (
    build_recognition_config,
    create_speech_client,
    load_speech_config,
)
from speech_models import response_to_chunks


def stream_with_language(
    audio_stream: Iterator[bytes], language_code: str = "en-US"
) -> Iterator[str]:
    client = create_speech_client()
    cfg = load_speech_config()
    cfg.language_code = language_code
    recognition_config = build_recognition_config(cfg)
    streaming_config = speech.StreamingRecognitionConfig(
        config=recognition_config,
        interim_results=True,
        single_utterance=False,
    )
    requests = (
        speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in audio_stream
    )
    for response in client.streaming_recognize(streaming_config, requests):
        for chunk in response_to_chunks(response):
            if chunk.text:
                yield chunk.text
