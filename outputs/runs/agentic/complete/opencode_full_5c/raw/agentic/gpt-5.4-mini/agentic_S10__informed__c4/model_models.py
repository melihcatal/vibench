import json
from dataclasses import dataclass


def normalize_text(text: str) -> str:
    return " ".join((text or "").split())


@dataclass
class LLMRequest:
    task: str
    input_text: str
    max_output_tokens: int


@dataclass
class LLMResponse:
    text: str


def parse_json_object(text: str) -> dict:
    return json.loads(text)
