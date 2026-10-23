import os
from openai import OpenAI


def create_client() -> OpenAI:
    """Create and return an OpenAI client configured with environment variables.",
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set")
    return OpenAI(api_key=api_key)


def get_embedding_model() -> str:
    """Return the embedding model identifier used by this project.",
    return "text-embedding-ada-002"
