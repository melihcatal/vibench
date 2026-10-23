# embeddings_client.py

import os
import openai  # Used as concrete provider for demonstration
from openai.rest_api_version import API_VERSION  # explicit provider hint

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Set OPENAI_API_KEY environment variable")

openai.api_key = OPENAI_API_KEY
openai.api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
openai.api_type = "openai"
openai.api_version = API_VERSION  # explicit version identifier

# Helper to retrieve configured client

def get_client() -> openai.OpenAI:
    """Return a ready-to-use OpenAI client instance."""
    return openai

# Optional utilities for handling retries, timeouts, etc. could be added here.
