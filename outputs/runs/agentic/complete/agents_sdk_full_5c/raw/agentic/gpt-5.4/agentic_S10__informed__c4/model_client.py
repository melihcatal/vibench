from __future__ import annotations

import json
import os
from typing import Dict, Iterable, Iterator, Optional

from openai import OpenAI

from model_models import ChatMessage, GenerationConfig, join_text_parts, usage_to_dict


OPENAI_DEFAULT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
OPENAI_JSON_MODEL = os.getenv("OPENAI_JSON_MODEL", OPENAI_DEFAULT_MODEL)
OPENAI_EMBED_MODEL = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")
OPENAI_TTS_MODEL = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")


def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return OpenAI(api_key=api_key)


def build_generation_config(**overrides: object) -> GenerationConfig:
    config = GenerationConfig(model=OPENAI_DEFAULT_MODEL)
    for key, value in overrides.items():
        if hasattr(config, key) and value is not None:
            setattr(config, key, value)
    return config


def create_chat_completion(
    messages: Iterable[ChatMessage],
    config: Optional[GenerationConfig] = None,
    response_format: Optional[Dict[str, str]] = None,
):
    cfg = config or build_generation_config()
    client = get_openai_client()
    params: Dict[str, object] = {
        "model": cfg.model,
        "messages": [message.as_openai() for message in messages],
        "temperature": cfg.temperature,
        "max_tokens": cfg.max_tokens,
        "top_p": cfg.top_p,
    }
    if response_format is not None:
        params["response_format"] = response_format
    return client.chat.completions.create(**params)


def stream_chat_completion(messages: Iterable[ChatMessage], config: Optional[GenerationConfig] = None) -> Iterator[str]:
    cfg = config or build_generation_config()
    client = get_openai_client()
    stream = client.chat.completions.create(
        model=cfg.model,
        messages=[message.as_openai() for message in messages],
        temperature=cfg.temperature,
        max_tokens=cfg.max_tokens,
        top_p=cfg.top_p,
        stream=True,
    )
    for chunk in stream:
        if not chunk.choices:
            continue
        delta = chunk.choices[0].delta
        text = getattr(delta, "content", None)
        if text:
            yield text


def extract_text_and_usage(response) -> Dict[str, object]:
    text = ""
    if response.choices:
        message = response.choices[0].message
        text = message.content or ""
    return {
        "text": text,
        "usage": usage_to_dict(getattr(response, "usage", None)),
        "model": getattr(response, "model", ""),
    }


def parse_json_object(text: str) -> Dict[str, object]:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(text[start : end + 1])
        raise


def collect_stream_text(chunks: Iterable[str]) -> str:
    return join_text_parts(chunks)
