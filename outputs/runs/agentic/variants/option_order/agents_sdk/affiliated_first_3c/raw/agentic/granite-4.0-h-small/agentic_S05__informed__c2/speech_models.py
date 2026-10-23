from typing import NamedTuple

# Simple data models for incoming STT WebSocket messages

class Alternatives(NamedTuple):
    transcript: str
    is_final: bool

class Result(NamedTuple):
    alternatives: list[Alternatives]

class RecognitionResponse(NamedTuple):
    results: list[Result]
