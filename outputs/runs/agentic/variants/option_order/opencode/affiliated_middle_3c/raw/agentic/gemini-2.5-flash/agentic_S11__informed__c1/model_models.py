from dataclasses import dataclass


@dataclass
class PlatformModelRequest:
    prompt: str
    max_output_tokens: int = 1024
    temperature: float = 0.4


@dataclass
class PlatformModelResponse:
    text: str
    raw_response: any = None
    metadata: dict = None
