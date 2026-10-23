import json
from typing import TypedDict, List, Any


class TextGenerationRequest(TypedDict):
    """Payload matching OpenAI text-generation request schema."""

    model: str
    messages: List[dict]
    temperature: float
    max_tokens: int


class TextGenerationChoice(TypedDict):
    """Response choice structure for OpenAI text-generation."""

    message: dict


class TextGenerationResponse(TypedDict):
    """Normalized response we expose internally."""

    choices: List[TextGenerationChoice]
    usage: dict


class JSONExtractionSchema(TypedDict):
    """Simple schema for JSON extraction – currently a placeholder."""

    type: str
    properties: dict
    required: List[str]


class JSONExtractionRequest(TypedDict):
    """Custom request type for extract_json helper."""

    text: str
    schema: JSONExtractionSchema


def normalize_request(req: Any) -> dict:
    """Convert our simple request objects to the concrete provider payload."""
    if isinstance(req, TextGenerationRequest):
        return {
            "model": req["model"],
            "messages": req["messages"],
            "temperature": req.get("temperature", 0.7),
            "max_tokens": req.get("max_tokens", 256),
        }
    elif isinstance(req, JSONExtractionRequest):
        # Build a system prompt that embeds the JSON schema
        schema_str = json.dumps(req["schema"], indent=2)
        messages = [
            {
                "role": "system",
                "content": f"You must output ONLY VALID JSON matching this schema:\\n{schema_str}",
            },
            {"role": "user", "content": req["text"]},
        ]
        return {
            "model": "gpt-4o-mini",
            "messages": messages,
            "temperature": 0.0,
            "max_tokens": 512,
        }
    raise TypeError(f"Unsupported request type: {type(req)}")
