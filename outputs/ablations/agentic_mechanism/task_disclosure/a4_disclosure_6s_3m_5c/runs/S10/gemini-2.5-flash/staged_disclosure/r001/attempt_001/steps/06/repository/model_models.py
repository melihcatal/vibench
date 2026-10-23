from dataclasses import dataclass, field
from typing import Dict, Any, Optional

@dataclass
class LLMRequest:
    prompt: str
    model: str
    temperature: float = 0.7
    max_tokens: int = 256
    stop_sequences: Optional[list[str]] = None
    top_p: float = 1.0
    top_k: int = 40

@dataclass
class LLMResponse:
    text: str
    model_id: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = field(default_factory=dict)

def normalize_response(raw_response: Dict[str, Any], model_id: Optional[str] = None) -> LLMResponse:
    """
    Normalizes a raw LLM provider response into a standard LLMResponse object.
    This is a placeholder and should be adapted to the specific LLM provider's response format.
    """
    generated_text = ""
    # Example: assuming the raw_response has a common structure like OpenAI's chat completions
    if "choices" in raw_response and len(raw_response["choices"]) > 0:
        first_choice = raw_response["choices"][0]
        if "text" in first_choice: # For older completion APIs
            generated_text = first_choice["text"]
        elif "message" in first_choice and "content" in first_choice["message"]: # For chat completions
            generated_text = first_choice["message"]["content"]
    elif "completion" in raw_response: # Another common pattern
        generated_text = raw_response["completion"]
    elif "generations" in raw_response and len(raw_response["generations"]) > 0: # Cohere-like
        generated_text = raw_response["generations"][0].get("text", "")
    elif "results" in raw_response and len(raw_response["results"]) > 0: # Generic for some APIs
        generated_text = raw_response["results"][0].get("text", "")


    return LLMResponse(text=generated_text, model_id=model_id, raw_response=raw_response)
