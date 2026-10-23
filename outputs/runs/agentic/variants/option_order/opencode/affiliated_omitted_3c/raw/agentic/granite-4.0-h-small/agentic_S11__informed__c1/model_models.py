from typing import TypedDict, Literal


class ModelResourceSpec(TypedDict):
    provider: str
    type: Literal["model", "deployment", "inference-profile"]
    id: str


class PlatformMetadata(TypedDict):
    provider: str
    request_id: str | None
    usage: dict | None
    handle: str | None
