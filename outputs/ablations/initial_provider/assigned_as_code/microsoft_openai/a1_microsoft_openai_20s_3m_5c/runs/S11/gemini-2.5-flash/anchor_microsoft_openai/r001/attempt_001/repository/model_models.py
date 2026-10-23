import dataclasses

@dataclasses.dataclass
class PlatformModelRequest:
    text: str

@dataclasses.dataclass
class PlatformModelResponse:
    text: str
    metadata: dict = dataclasses.field(default_factory=dict)
