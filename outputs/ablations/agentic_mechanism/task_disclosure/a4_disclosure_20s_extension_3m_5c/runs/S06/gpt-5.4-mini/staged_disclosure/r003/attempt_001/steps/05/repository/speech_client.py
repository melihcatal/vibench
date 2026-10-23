import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

DEFAULT_TTS_MODEL = "gpt-4o-mini-tts"
DEFAULT_TTS_VOICE = "alloy"
DEFAULT_OUTPUT_FORMAT = "mp3"


@dataclass(frozen=True)
class SpeechConfig:
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model: str = DEFAULT_TTS_MODEL
    voice: str = DEFAULT_TTS_VOICE
    response_format: str = DEFAULT_OUTPUT_FORMAT

    @classmethod
    def from_env(cls) -> "SpeechConfig":
        return cls(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL"),
            model=os.getenv("OPENAI_TTS_MODEL", DEFAULT_TTS_MODEL),
            voice=os.getenv("OPENAI_TTS_VOICE", DEFAULT_TTS_VOICE),
            response_format=os.getenv("OPENAI_TTS_FORMAT", DEFAULT_OUTPUT_FORMAT),
        )


def build_client(config: Optional[SpeechConfig] = None) -> Any:
    cfg = config or SpeechConfig.from_env()
    if OpenAI is None:
        raise RuntimeError("openai package is required for speech synthesis")
    kwargs: Dict[str, str] = {}
    if cfg.api_key:
        kwargs["api_key"] = cfg.api_key
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    return OpenAI(**kwargs)


def get_tts_config() -> Dict[str, str]:
    cfg = SpeechConfig.from_env()
    return {
        "model": cfg.model,
        "voice": cfg.voice,
        "response_format": cfg.response_format,
    }


def synthesize_text(client: Any, text: str, config: Optional[SpeechConfig] = None) -> bytes:
    cfg = config or SpeechConfig.from_env()
    response = client.audio.speech.create(
        model=cfg.model,
        voice=cfg.voice,
        input=text,
        response_format=cfg.response_format,
    )
    return response.read()


def synthesize_ssml(client: Any, ssml: str, config: Optional[SpeechConfig] = None) -> bytes:
    return synthesize_text(client, ssml, config=config)
