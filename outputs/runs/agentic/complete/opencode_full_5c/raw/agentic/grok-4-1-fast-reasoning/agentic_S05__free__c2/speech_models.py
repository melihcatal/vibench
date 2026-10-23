from typing import TypedDict, AsyncGenerator, Any


class STTResult(TypedDict):
    transcript: str
    is_final: bool


STTStream = AsyncGenerator[STTResult, None]
