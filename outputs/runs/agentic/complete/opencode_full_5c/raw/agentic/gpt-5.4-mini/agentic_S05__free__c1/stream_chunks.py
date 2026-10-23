from typing import AsyncIterable, AsyncIterator

from google.cloud import speech_v1 as speech

from speech_client import (
    build_recognition_config,
    create_speech_client,
    load_speech_config,
)
from speech_models import response_to_chunks


async def stream_chunks(audio_chunks: AsyncIterable[bytes]) -> AsyncIterator[str]:
    client = create_speech_client()
    cfg = load_speech_config()
    streaming_config = speech.StreamingRecognitionConfig(
        config=build_recognition_config(cfg),
        interim_results=True,
        single_utterance=False,
    )

    def reqs():
        for chunk in audio_chunks:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    for response in client.streaming_recognize(streaming_config, reqs()):
        for item in response_to_chunks(response):
            if item.text:
                yield item.text
