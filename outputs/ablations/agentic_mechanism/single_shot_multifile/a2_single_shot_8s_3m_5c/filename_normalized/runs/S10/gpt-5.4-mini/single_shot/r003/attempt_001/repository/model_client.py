import os
from functools import lru_cache
from openai import OpenAI

_DEFAULT_MODELS = {
    "summarize": "gpt-4.1-mini",
    "extract": "gpt-4.1-mini",
    "qa": "gpt-4.1",
    "stream": "gpt-4.1-mini",
    "safety": "gpt-4.1-mini",
    "translate": "gpt-4.1-mini",
    "embed": "text-embedding-3-small",
    "speech": "gpt-4o-mini",
}


@lru_cache(maxsize=1)
def get_text_client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def resolve_text_model(model: str | None, task: str) -> str:
    if model:
        return model
    return os.environ.get(f"OPENAI_{task.upper()}_MODEL", _DEFAULT_MODELS[task])


def resolve_embedding_model(model: str | None = None) -> str:
    if model:
        return model
    return os.environ.get("OPENAI_EMBEDDING_MODEL", _DEFAULT_MODELS["embed"])


def resolve_audio_model(model: str | None = None) -> str:
    if model:
        return model
    return os.environ.get("OPENAI_AUDIO_MODEL", _DEFAULT_MODELS["speech"])
