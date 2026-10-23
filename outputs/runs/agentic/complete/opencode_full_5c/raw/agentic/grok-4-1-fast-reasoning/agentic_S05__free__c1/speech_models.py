from typing import TypedDict


class Transcript(TypedDict):
    text: str
    is_final: bool
    confidence: float | None
