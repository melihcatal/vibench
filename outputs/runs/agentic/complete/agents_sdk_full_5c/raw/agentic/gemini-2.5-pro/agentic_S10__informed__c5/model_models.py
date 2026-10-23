from dataclasses import dataclass
from typing import Any

@dataclass
class ModelRequest:
    prompt: str
    context: str = ""
    json_mode: bool = False

@dataclass
class ModelResponse:
    text: str
    raw_response: Any = None

@dataclass
class StreamChunk:
    text: str
    raw_chunk: Any = None
