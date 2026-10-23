import os
from functools import lru_cache

from google.cloud import vision_v1, documentai_v1
import openai
import anthropic
import cohere
import deepl

@lru_cache(maxsize=1)
def get_gcp_vision_client() -> vision_v1.ImageAnnotatorClient:
    """Provides a cached Google Cloud Vision API client."""
    return vision_v1.ImageAnnotatorClient()

def get_gcp_documentai_processor_path(
    project_id: str,
    location: str,
    processor_id: str
) -> str:
    """Constructs the full resource path for a Document AI processor."""
    return f"projects/{project_id}/locations/{location}/processors/{processor_id}"

@lru_cache(maxsize=1)
def get_openai_client() -> openai.OpenAI:
    """Provides a cached OpenAI client, loading API key from environment."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    return openai.OpenAI(api_key=api_key)

@lru_cache(maxsize=1)
def get_anthropic_client() -> anthropic.Anthropic:
    """Provides a cached Anthropic client, loading API key from environment."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")
    return anthropic.Anthropic(api_key=api_key)

@lru_cache(maxsize=1)
def get_cohere_client() -> cohere.Client:
    """Provides a cached Cohere client, loading API key from environment."""
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")
    return cohere.Client(api_key=api_key)

@lru_cache(maxsize=1)
def get_deepl_translator() -> deepl.Translator:
    """Provides a cached DeepL Translator client, loading API key from environment."""
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")
    return deepl.Translator(auth_key)
