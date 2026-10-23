import dataclasses
from typing import Any, Dict, List, Optional

@dataclasses.dataclass
class ModelRequest:
    model: str
    prompt: str
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 500
    top_p: Optional[float] = 1.0
    stop_sequences: Optional[List[str]] = None
    provider_name: str = "google" # Example provider

@dataclasses.dataclass
class ModelResponse:
    text: str
    model: str
    raw_response: Optional[Dict[str, Any]] = None

def normalize_response(raw_response: Dict[str, Any], model_name: str) -> ModelResponse:
    """Normalizes a raw LLM response into a standard ModelResponse object."""
    if "candidates" in raw_response and raw_response["candidates"]:
        # Assuming a structure similar to Google's Generative AI
        text = raw_response["candidates"][0]["content"]["parts"][0]["text"]
        return ModelResponse(text=text, model=model_name, raw_response=raw_response)
    elif "choices" in raw_response and raw_response["choices"]:
        # Assuming a structure similar to OpenAI
        text = raw_response["choices"][0]["text"]
        return ModelResponse(text=text, model=model_name, raw_response=raw_response)
    else:
        raise ValueError("Unsupported raw response format")

def get_model_family_for_model(model_name: str) -> str:
    """Returns the model family for a given model name."""
    if "gemini" in model_name.lower():
        return "gemini"
    elif "gpt" in model_name.lower():
        return "gpt"
    else:
        return "unknown"
