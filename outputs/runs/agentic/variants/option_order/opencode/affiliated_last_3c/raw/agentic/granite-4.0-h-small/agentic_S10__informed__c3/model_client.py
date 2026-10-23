import os
from anthropic import Anthropic  # type: ignore

# Central configuration for hosted LLM inference
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise RuntimeError("ANTHROPIC_API_KEY environment variable not set")

# Create a reusable Anthropic client instance
client = Anthropic(api_key=ANTHROPIC_API_KEY)


def create_client() -> Anthropic:
    """Factory to create and return a configured Anthropic client.
    This allows loading configuration (API key, endpoint, etc.)
    in one place and reusing the client throughout the service.
    """
    return Anthropic(api_key=ANTHROPIC_API_KEY)
