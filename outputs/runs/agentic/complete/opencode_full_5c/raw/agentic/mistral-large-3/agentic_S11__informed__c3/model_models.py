from typing import Dict, Any, Optional, List
from pydantic import BaseModel


class ModelRequest(BaseModel):
    """Request payload for Bedrock model invocation."""

    prompt: str
    model_id: str
    inference_parameters: Optional[Dict[str, Any]] = None


class ModelResponse(BaseModel):
    """Response payload from Bedrock model invocation."""

    output_text: str
    token_count: int
    input_token_count: int
    stop_reason: Optional[str] = None


class ModelMetadata(BaseModel):
    """Metadata associated with a Bedrock model response."""

    model_id: str
    input_tokens: int
    output_tokens: int
    latency: float
    provider: str


def normalize_request(
    prompt: str, model_id: str, parameters: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Normalize request payload for Bedrock."""
    return {"inputText": prompt, "textGenerationConfig": parameters or {}}


def normalize_response(response_body: Dict[str, Any]) -> ModelResponse:
    """Normalize response from Bedrock."""
    results = response_body.get("results", [{}])[0]
    return ModelResponse(
        output_text=results.get("outputText", ""),
        token_count=results.get("tokenCount", 0),
        input_token_count=response_body.get("inputTextTokenCount", 0),
        stop_reason=results.get("stopReason"),
    )
