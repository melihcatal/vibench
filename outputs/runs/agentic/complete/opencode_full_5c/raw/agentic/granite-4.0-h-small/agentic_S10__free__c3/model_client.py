import os
from typing import Literal, TypedDict

# Example configuration for hosted model inference (OpenAI API)
MODEL_PROVIDER = "openai"  # Identifier used in code comments
MODEL_ENDPOINT = "https://api.openai.com/v1"


class ModelConfig(TypedDict):
    provider: Literal["openai"]
    api_key: str
    max_tokens: int
    temperature: float


def load_config() -> ModelConfig:
    """Load local configuration for the hosted LLM.

    Reads the OPENAI_API_KEY environment variable and returns a
    configuration dictionary compatible with the ModelClient.
    """
    if MODEL_PROVIDER != "openai":
        raise ValueError(f"Unsupported provider: {MODEL_PROVIDER}")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set")
    return ModelConfig(
        provider=MODEL_PROVIDER,
        api_key=api_key,
        max_tokens=256,
        temperature=0.7,
    )


# Simple wrapper that exposes a streaming method
# to be used by other files.
class ModelClient:
    def __init__(self, model_name: str = "gpt-4o-mini") -> None:
        self.config = load_config()
        self.model_name = model_name

    def complete(self, prompt: str) -> dict:
        """Perform a synchronous completion request to the provider.

        Returns:
            dict: Raw JSON response from the provider.
        """
        # Placeholder for actual HTTP request logic.
        # In production you would use `openai` or `requests` lib here.
        return {
            "text": f"{prompt} -- generated continuation",
            "usage": {},
        }

    def stream_complete(self, prompt: str) -> str:
        """Simulate streaming token generation.
        Here we just concatenate the prompt with a placeholder.
        """
        return f"Streaming response for: {prompt}"
