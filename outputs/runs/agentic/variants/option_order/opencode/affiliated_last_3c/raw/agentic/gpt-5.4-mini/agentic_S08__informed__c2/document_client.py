import os
from pathlib import Path
from typing import Optional


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(name)
    return value


def load_document_bytes(source: str) -> bytes:
    if source.startswith('http://') or source.startswith('https://'):
        import requests
        return requests.get(source, timeout=60).content
    return Path(source).read_bytes()


def normalize_language(locale: Optional[str]) -> Optional[str]:
    return locale.strip() if locale else None
