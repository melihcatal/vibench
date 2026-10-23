from typing import Iterable, Iterator

from google.cloud import speech

from speech_client import (
    build_speech_client,
    build_streaming_config,
    load_stream_config,
)


def stream_microphone(audio_chunks: Iterable[bytes]) -> Iterator[str]:
    client = build_speech_client()
    config = build_streaming_config(load_stream_config())
    requests = (
        speech.StreamingRecognizeRequest(audio_content=chunk)
        for chunk in audio_chunks
        if chunk
    )
    responses = client.streaming_recognize(config=config, requests=requests)
    for response in responses:
        for result in response.results:
            if result.alternatives:
                yield result.alternatives[0].transcript
