
import dataclasses
from typing import Any, Dict, List, Optional

@dataclasses.dataclass
class LLMRequest:
    """Represents a standardized request for LLM inference."""
    prompt: str
    model_id: str
    temperature: float = 0.7
    max_tokens: int = 100
    top_p: float = 1.0
    stop_sequences: Optional[List[str]] = None
    stream: bool = False
    extra_params: Optional[Dict[str, Any]] = None

@dataclasses.dataclass
class LLMResponse:
    """Represents a standardized response from LLM inference."""
    generated_text: str
    model_id: str
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    finish_reason: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

def normalize_prompt(prompt: Any) -> str:
    """Normalizes a prompt to a string format."""
    if not isinstance(prompt, str):
        return str(prompt).strip()
    return prompt.strip()

def normalize_model_id(generic_model_name: str, provider_mapping: Dict[str, str]) -> str:
    """
    Normalizes a generic model name to a provider-specific model ID.

    Args:
        generic_model_name: The generic name of the model (e.g., "gpt-4", "claude-3").
        provider_mapping: A dictionary mapping generic names to provider-specific IDs.

    Returns:
        The provider-specific model ID.
    """
    return provider_mapping.get(generic_model_name, generic_model_name)

def normalize_llm_response(
    raw_response: Dict[str, Any],
    model_id: str,
    provider_type: str
) -> LLMResponse:
    """
    Normalizes a raw LLM provider response into a standardized LLMResponse object.

    Args:
        raw_response: The raw response dictionary from the LLM provider.
        model_id: The identifier of the model that generated the response.
        provider_type: A string indicating the LLM provider (e.g., "openai", "anthropic").

    Returns:
        An LLMResponse object.
    """
    generated_text = ""
    prompt_tokens = None
    completion_tokens = None
    total_tokens = None
    finish_reason = None
    error = None

    if provider_type == "openai":
        try:
            if "choices" in raw_response and raw_response["choices"]:
                generated_text = raw_response["choices"][0].get("message", {}).get("content", "")
                finish_reason = raw_response["choices"][0].get("finish_reason")
            if "usage" in raw_response:
                prompt_tokens = raw_response["usage"].get("prompt_tokens")
                completion_tokens = raw_response["usage"].get("completion_tokens")
                total_tokens = raw_response["usage"].get("total_tokens")
        except KeyError as e:
            error = f"Error parsing OpenAI response: {e}"
    elif provider_type == "anthropic":
        try:
            if "content" in raw_response and raw_response["content"]:
                # Anthropic's new messages API returns content as a list of dicts
                for item in raw_response["content"]:
                    if item["type"] == "text":
                        generated_text += item["text"]
                finish_reason = raw_response.get("stop_reason")
            if "usage" in raw_response:
                prompt_tokens = raw_response["usage"].get("input_tokens")
                completion_tokens = raw_response["usage"].get("output_tokens")
                total_tokens = prompt_tokens + completion_tokens if prompt_tokens is not None and completion_tokens is not None else None
        except KeyError as e:
            error = f"Error parsing Anthropic response: {e}"
    elif provider_type == "google":
        try:
            if "candidates" in raw_response and raw_response["candidates"]:
                # Assuming text-based generation for simplicity
                generated_text = raw_response["candidates"][0].get("content", {}).get("parts", [{}])[0].get("text", "")
                finish_reason = raw_response["candidates"][0].get("finishReason")
            # Google's API might have token counts in a different structure or not at all for some models/APIs
            # This part might need adjustment based on the specific Google LLM API used (e.g., Gemini vs PaLM)
            # For now, leaving token counts as None.
        except KeyError as e:
            error = f"Error parsing Google response: {e}"
    else:
        error = f"Unsupported provider type: {provider_type}"
        generated_text = str(raw_response) # Fallback to raw response as text if unknown provider

    return LLMResponse(
        generated_text=generated_text,
        model_id=model_id,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=total_tokens,
        finish_reason=finish_reason,
        raw_response=raw_response,
        error=error
    )
