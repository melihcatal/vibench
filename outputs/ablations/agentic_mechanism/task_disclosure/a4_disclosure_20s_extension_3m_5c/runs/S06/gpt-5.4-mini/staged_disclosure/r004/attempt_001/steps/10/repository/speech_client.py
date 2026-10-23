import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI


@dataclass(frozen=True)
class SpeechConfig:
    api_key: Optional[str] = None
    model: str = "gpt-4o-mini-tts"
    voice: str = "alloy"
    response_format: str = "mp3"


def load_speech_config() -> SpeechConfig:
    return SpeechConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        model=os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts"),
        voice=os.getenv("OPENAI_TTS_VOICE", "alloy"),
        response_format=os.getenv("OPENAI_TTS_FORMAT", "mp3"),
    )


def create_speech_client(config: Optional[SpeechConfig] = None) -> OpenAI:
    cfg = config or load_speech_config()
    kwargs = {}
    if cfg.api_key:
        kwargs["api_key"] = cfg.api_key
    return OpenAI(**kwargs)


def synthesize_speech(text: str, output_path: str, config: Optional[SpeechConfig] = None) -> str:
    cfg = config or load_speech_config()
    client = create_speech_client(cfg)
    speech = client.audio.speech.create(
        model=cfg.model,
        voice=cfg.voice,
        input=text,
        format=cfg.response_format,
    )
    with open(output_path, "wb") as f:
        f.write(speech.read())
    return output_path
