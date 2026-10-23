import os
from dataclasses import dataclass, field
from typing import Optional

from deepgram import DeepgramClient, DeepgramClientOptions


DEEPGRAM_API_HOST = "api.deepgram.com"

DEFAULT_MODEL = "nova-2"
DEFAULT_LANGUAGE = "en-US"
DEFAULT_SAMPLE_RATE = 16000
DEFAULT_CHANNELS = 1
DEFAULT_ENCODING = "linear16"


@dataclass
class StreamConfig:
    model: str = DEFAULT_MODEL
    language: str = DEFAULT_LANGUAGE
    sample_rate: int = DEFAULT_SAMPLE_RATE
    channels: int = DEFAULT_CHANNELS
    encoding: str = DEFAULT_ENCODING
    interim_results: bool = True
    punctuate: bool = True
    profanity_filter: bool = False
    smart_format: bool = True
    vad_events: bool = True
    endpointing: Optional[int] = None
    extra: dict = field(default_factory=dict)

    def to_deepgram_options(self) -> dict:
        options = {
            "model": self.model,
            "language": self.language,
            "encoding": self.encoding,
            "sample_rate": self.sample_rate,
            "channels": self.channels,
            "punctuate": self.punctuate,
            "interim_results": self.interim_results,
            "smart_format": self.smart_format,
            "vad_events": self.vad_events,
        }
        if self.profanity_filter:
            options["profanity_filter"] = True
        if self.endpointing is not None:
            options["endpointing"] = self.endpointing
        options.update(self.extra)
        return options


def load_api_key() -> str:
    api_key = os.environ.get("DEEPGRAM_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "DEEPGRAM_API_KEY environment variable is required for Deepgram Streaming API"
        )
    return api_key


def create_deepgram_client(api_key: Optional[str] = None) -> DeepgramClient:
    key = api_key or load_api_key()
    options = DeepgramClientOptions(
        url=f"wss://{DEEPGRAM_API_HOST}/v1/listen",
        options={"keepalive": "true"},
    )
    return DeepgramClient(key, options)


def create_listen_connection(
    client: DeepgramClient, config: Optional[StreamConfig] = None
):
    cfg = config or StreamConfig()
    return client.listen.live.v("1"), cfg.to_deepgram_options()
