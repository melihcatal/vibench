import os
from dataclasses import asdict
from typing import Optional

from deepgram import DeepgramClient, LiveOptions

from speech_models import StreamConfig


def load_config() -> StreamConfig:
    return StreamConfig(
        language=os.getenv("STT_LANGUAGE"),
        punctuation=os.getenv("STT_PUNCTUATION", "true").lower() in {"1", "true", "yes", "on"},
        interim_results=os.getenv("STT_INTERIM_RESULTS", "true").lower() in {"1", "true", "yes", "on"},
    )


def create_client() -> DeepgramClient:
    api_key = os.environ["DEEPGRAM_API_KEY"]
    return DeepgramClient(api_key)


def live_options(config: Optional[StreamConfig] = None) -> LiveOptions:
    config = config or load_config()
    payload = {
        "model": os.getenv("DEEPGRAM_MODEL", "nova-2"),
        "punctuate": config.punctuation,
        "interim_results": config.interim_results,
    }
    if config.language:
        payload["language"] = config.language
    return LiveOptions(**payload)
