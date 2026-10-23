from typing import Iterator

from google.cloud import speech_v1p1beta1 as speech

from speech_client import build_client, load_config, streaming_config


def stream_with_language(language_code: str, enable_punctuation: bool = True) -> Iterator[str]:
    client = build_client()
    config = load_config()
    config.language_code = language_code
    config.enable_punctuation = enable_punctuation
    responses = client.streaming_recognize(streaming_config(config), iter(()))
    for response in responses:
        for result in response.results:
            if result.alternatives:
                yield result.alternatives[0].transcript
