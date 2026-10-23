import os
from dataclasses import dataclass
from typing import Optional

from deepgram import DeepgramClient, LiveOptions


@dataclass
class SpeechConfig:
    api_key: str
    model: str = "nova-2"
    language: Optional[str] = None
    punctuate: bool = True


def load_speech_config() -> SpeechConfig:
    return SpeechConfig(
        api_key=os.environ.get("DEEPGRAM_API_KEY", ""),
        model=os.environ.get("DEEPGRAM_MODEL", "nova-2"),
        language=os.environ.get("DEEPGRAM_LANGUAGE"),
    )


def create_deepgram_client(config: Optional[SpeechConfig] = None) -> DeepgramClient:
    cfg = config or load_speech_config()
    return DeepgramClient(cfg.api_key)


def build_live_options(config: Optional[SpeechConfig] = None) -> LiveOptions:
    cfg = config or load_speech_config()
    kwargs = {
        "model": cfg.model,
        "punctuate": cfg.punctuate,
        "interim_results": True,
        "smart_format": True,
    }
    if cfg.language:
        kwargs["language"] = cfg.language
    return LiveOptions(**kwargs)
