import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env if present

# -----------------------------------
# Provider configuration (choose ONE)
# -----------------------------------

# Example: OpenAI Embeddings (replace with your chosen provider's config)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Set OPENAI_API_KEY environment variable")

# SDK import (OpenAI SDK in this example)
import openai

openai.api_key = OPENAI_API_KEY

# Helper to return the configured embedder


def get_embedder() -> openai:
    """Return an initialized embedder client for the selected provider."""
    return openai
