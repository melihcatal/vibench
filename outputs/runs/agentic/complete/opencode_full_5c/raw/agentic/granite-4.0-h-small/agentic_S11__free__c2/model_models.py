from typing import TypedDict, List, Dict, Any


class PlatformRequest(TypedDict):
    prompt: str
    temperature: float
    max_tokens: int


class PlatformResponse(TypedDict):
    choices: List[Dict[str, Any]]
    usage: Dict[str, int]


class NormalizedResponse(TypedDict):
    output: str
    usage: Dict[str, int]
    provider: str


def normalize_response(raw: PlatformResponse) -> NormalizedResponse:
    # Extract the first choice and its content
    choice = raw.get("choices", [{}])[0]
    content = choice.get("text", "")
    usage = raw.get("usage", {})
    return NormalizedResponse(
        output=content, usage=usage, provider=raw.get("provider", "unknown")
    )
