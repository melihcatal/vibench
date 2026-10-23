import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI


@dataclass
class SpeechSettings:
    model: str
    language: Optional[str] = None
    punctuation: bool = True


def load_speech_settings(model: str = "gpt-4o-mini-transcribe") -> SpeechSettings:
    language = os.getenv("OPENAI_TRANSCRIBE_LANGUAGE")
    punctuation = os.getenv("OPENAI_TRANSCRIBE_PUNCTUATION", "true").lower() not in {"0", "false", "no"}
    return SpeechSettings(model=model, language=language, punctuation=punctuation)


def create_openai_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
