from typing import TypedDict

class EmbedRequest(TypedDict):
    model: str
    input: str | list[str]
    dimension: int | None

class EmbedResponse(TypedDict):
    embedding: list[float]
