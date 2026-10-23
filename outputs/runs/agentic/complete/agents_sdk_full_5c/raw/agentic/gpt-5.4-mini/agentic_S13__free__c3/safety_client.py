import os
from dataclasses import dataclass
from typing import Optional

import google.generativeai as genai

GOOGLE_API_KEY_ENV = "GOOGLE_API_KEY"
DEFAULT_MODEL = "gemini-1.5-pro"
DEFAULT_EMBED_MODEL = "text-embedding-004"
DEFAULT_TTS_VOICE = "Kore"


@dataclass
class SafetyClientConfig:
    api_key: Optional[str] = None
    model: str = DEFAULT_MODEL
    embed_model: str = DEFAULT_EMBED_MODEL
    tts_voice: str = DEFAULT_TTS_VOICE


def load_config() -> SafetyClientConfig:
    return SafetyClientConfig(
        api_key=os.getenv(GOOGLE_API_KEY_ENV),
        model=os.getenv("SAFETY_MODEL", DEFAULT_MODEL),
        embed_model=os.getenv("SAFETY_EMBED_MODEL", DEFAULT_EMBED_MODEL),
        tts_voice=os.getenv("SAFETY_TTS_VOICE", DEFAULT_TTS_VOICE),
    )


def configure_client(config: Optional[SafetyClientConfig] = None) -> SafetyClientConfig:
    cfg = config or load_config()
    if cfg.api_key:
        genai.configure(api_key=cfg.api_key)
    return cfg


def generative_model(model_name: Optional[str] = None):
    cfg = configure_client()
    return genai.GenerativeModel(model_name or cfg.model)


def embedder(model_name: Optional[str] = None):
    cfg = configure_client()
    return model_name or cfg.embed_model
