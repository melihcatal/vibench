from __future__ import annotations

from typing import Iterable

from google.cloud import speech

from speech_client import create_speech_client, load_config, streaming_config


def stream_with_language(language_code: str = "en-US", enable_punctuation: bool = True) -> Iterable[str]:
    client = create_speech_client()
    cfg = load_config()
    cfg = cfg.__class__(
        project_id=cfg.project_id,
        location=cfg.location,
        model=cfg.model,
        language_code=language_code,
        punctuation=enable_punctuation,
    )
    config = streaming_config(cfg)
    requests = iter(())
    responses = client.streaming_recognize(config, requests)
    for response in responses:
        for result in response.results:
            if result.alternatives:
                yield result.alternatives[0].transcript
