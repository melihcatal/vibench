from typing import List, Any, Iterator
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str = Field(..., pattern="^(system|user|assistant)$")
    content: str


def normalize_openai_chat(resp: Any) -> str:
    return resp.choices[0].message.content.strip()


def normalize_anthropic_chat(resp: Any) -> str:
    return resp.content[0].text.strip()


def normalize_google_chat(resp: Any) -> str:
    return resp.text.strip()


def normalize_mistral_chat(resp: Any) -> str:
    return resp.choices[0].message.content.strip()


def normalize_stream_chunk(chunk: Any) -> str:
    delta = chunk.choices[0].delta.content
    return delta if delta else ""
