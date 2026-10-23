from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class LLMRequest:
    """Normalized request payload for hosted LLM inference.

    Args:
        provider (str): Identifier of the LLM provider (e.g., 'dashscope').
        model (str): Model identifier used by the provider (e.g., 'qwen-plus').
        messages (List[Dict[str, Any]]): Messages formatted per provider SDK.
        max_tokens (int, optional): Max tokens for generation.
        temperature (float, optional): Sampling temperature.
    """

    provider: str
    model: str
    messages: List[Dict[str, Any]]
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None


@dataclass
class LLMResponse:
    """Standardized response from a hosted LLM.

    Args:
        success (bool): Whether the call succeeded.
        content (str): Generated text output.
        json (Optional[Dict[str, Any]]): Parsed JSON output if applicable.
        raw (Any): Raw SDK response object (for debugging).
    """

    success: bool
    content: str
    json: Optional[Dict[str, Any]] = None
    raw: Any = None


def normalize_response(raw_resp: Any, provider: str) -> LLMResponse:
    """Convert provider-specific SDK response to a unified LLMResponse.

    Args:
        raw_resp (Any): Raw response from the underlying SDK (dashscope, openai, etc.).
        provider (str): The provider name for routing.

    Returns:
        LLMResponse: Unified representation.
    """
    if provider in ("dashscope", "mistral", "anthropic", "gemini", "openai"):
        try:
            message = raw_resp.choices[0].message.content
            return LLMResponse(success=True, content=message)
        except Exception as e:
            return LLMResponse(success=False, content=str(e), raw=raw_resp)
    elif provider == "bedrock":
        try:
            # Bedrock returns raw text in raw_resp
            return LLMResponse(success=True, content=raw_resp)
        except Exception as e:
            return LLMResponse(success=False, content=str(e), raw=raw_resp)
    else:
        return LLMResponse(success=False, content="Unsupported provider", raw=raw_resp)
