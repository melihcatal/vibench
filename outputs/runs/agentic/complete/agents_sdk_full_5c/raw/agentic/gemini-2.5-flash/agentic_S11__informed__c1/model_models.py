from typing import Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class ModelRequest:
    """Defines a simple request structure for a generative model."""
    prompt: str
    model_name: str = "gemini-pro"
    temperature: float = 0.7
    max_output_tokens: int = 1024

@dataclass
class ModelResponse:
    """Defines a simple response structure for a generative model."""
    text: str
    finish_reason: Optional[str] = None
    usage_metadata: Optional[Dict[str, Any]] = None
    raw_response: Optional[Any] = None # To store the raw provider response object

if __name__ == '__main__':
    # Example usage
    request = ModelRequest(prompt="Tell me a joke.", temperature=0.9)
    print(f"Model Request: {request}")

    response = ModelResponse(
        text="Why don't scientists trust atoms? Because they make up everything!",
        finish_reason="STOP",
        usage_metadata={"input_token_count": 8, "output_token_count": 15}
    )
    print(f"Model Response: {response}")
