import os
from functools import lru_cache

import openai


@lru_cache(maxsize=1)
def get_api_key():
    return os.getenv("OPENAI_API_KEY", "")


@lru_cache(maxsize=1)
def get_client():
    return openai.OpenAI(api_key=get_api_key())


def get_audio_model():
    return os.getenv("OPENAI_TRANSCRIBE_MODEL", "gpt-4o-mini-transcribe")


def get_text_model():
    return os.getenv("OPENAI_TEXT_MODEL", "gpt-4o-mini")


def get_embedding_model():
    return os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def normalize_text(value):
    if value is None:
        return ""
    return " ".join(str(value).split())


def segments_from_result(result):
    segments = []
    for item in getattr(result, "segments", []) or []:
        segments.append(
            {
                "start": getattr(item, "start", None),
                "end": getattr(item, "end", None),
                "text": normalize_text(getattr(item, "text", "")),
            }
        )
    return segments
