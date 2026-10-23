import os
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional

from openai import OpenAI


def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return OpenAI(api_key=api_key)


@contextmanager
def resolve_audio_path(audio_path: str) -> Iterator[str]:
    path = Path(audio_path).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(str(path))
    yield str(path)
