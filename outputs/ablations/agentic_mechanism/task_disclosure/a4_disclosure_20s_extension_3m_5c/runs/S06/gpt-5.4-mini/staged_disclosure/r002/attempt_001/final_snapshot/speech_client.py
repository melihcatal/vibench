from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI

DEFAULT_TTS_MODEL = os.getenv('OPENAI_TTS_MODEL', 'gpt-4o-mini-tts')
DEFAULT_VOICE = os.getenv('OPENAI_TTS_VOICE', 'alloy')
DEFAULT_RESPONSE_FORMAT = os.getenv('OPENAI_TTS_FORMAT', 'mp3')


@dataclass(frozen=True)
class SpeechConfig:
    api_key: Optional[str] = None
    organization: Optional[str] = None
    project: Optional[str] = None
    base_url: Optional[str] = None
    model: str = DEFAULT_TTS_MODEL
    voice: str = DEFAULT_VOICE
    response_format: str = DEFAULT_RESPONSE_FORMAT

    @classmethod
    def from_env(cls) -> 'SpeechConfig':
        return cls(
            api_key=os.getenv('OPENAI_API_KEY'),
            organization=os.getenv('OPENAI_ORG_ID') or os.getenv('OPENAI_ORGANIZATION'),
            project=os.getenv('OPENAI_PROJECT_ID') or os.getenv('OPENAI_PROJECT'),
            base_url=os.getenv('OPENAI_BASE_URL'),
            model=os.getenv('OPENAI_TTS_MODEL', DEFAULT_TTS_MODEL),
            voice=os.getenv('OPENAI_TTS_VOICE', DEFAULT_VOICE),
            response_format=os.getenv('OPENAI_TTS_FORMAT', DEFAULT_RESPONSE_FORMAT),
        )


def build_client(config: Optional[SpeechConfig] = None) -> OpenAI:
    cfg = config or SpeechConfig.from_env()
    kwargs = {}
    if cfg.api_key:
        kwargs['api_key'] = cfg.api_key
    if cfg.organization:
        kwargs['organization'] = cfg.organization
    if cfg.project:
        kwargs['project'] = cfg.project
    if cfg.base_url:
        kwargs['base_url'] = cfg.base_url
    return OpenAI(**kwargs)


def create_tts_request(text: str, config: Optional[SpeechConfig] = None, *, instructions: Optional[str] = None):
    cfg = config or SpeechConfig.from_env()
    client = build_client(cfg)
    params = {
        'model': cfg.model,
        'voice': cfg.voice,
        'input': text,
        'response_format': cfg.response_format,
    }
    if instructions:
        params['instructions'] = instructions
    return client.audio.speech.create(**params)


def speech_settings() -> SpeechConfig:
    return SpeechConfig.from_env()
