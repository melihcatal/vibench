import os
from dataclasses import dataclass
from typing import Optional
import openai

@dataclass
class SpeechClientConfig:
    openai_api_key: Optional[str] = None
    openai_organization: Optional[str] = None
    model: str = "gpt-4o-mini"
    language: str = "en"
    punctuate: bool = True


def load_config() -> SpeechClientConfig:
    return SpeechClientConfig(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_organization=os.getenv("OPENAI_ORG_ID"),
        model=os.getenv("OPENAI_STT_MODEL", "gpt-4o-mini"),
        language=os.getenv("SPEECH_LANGUAGE", "en"),
        punctuate=os.getenv("SPEECH_PUNCTUATE", "1") not in {"0", "false", "False"},
    )


def build_client(config: Optional[SpeechClientConfig] = None) -> openai.OpenAI:
    cfg = config or load_config()
    return openai.OpenAI(api_key=cfg.openai_api_key, organization=cfg.openai_organization)
