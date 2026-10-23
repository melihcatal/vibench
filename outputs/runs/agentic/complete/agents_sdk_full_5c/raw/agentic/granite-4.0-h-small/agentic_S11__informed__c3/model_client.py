# model_client.py
# Local helper: Configuration and client utilities for Managed Model Platform Workflow

import os
from google.cloud import generativeai as genai

# ---------------------------------------------------------------------------
# Provider-specific configuration (Google Vertex AI generative models)
# ---------------------------------------------------------------------------
GOOGLE_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "my-vertex-project")
LOCATION = os.getenv("LOCATION", "us-central1")
CREDENTIAL_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "/path/to/vertex-credentials.json")

# Optional: default model family to use when none is supplied
DEFAULT_MODEL_FAMILY = os.getenv("DEFAULT_MODEL_FAMILY", "gemini-1.5-flash")

# ---------------------------------------------------------------------------
# Client helper utilities
# ---------------------------------------------------------------------------

def configure_client() -> None:
    """Configure the Vertex AI generative AI client using environment settings."""
    genai.configure(project=GOOGLE_PROJECT, location=LOCATION)
    # Load credentials from file if specified
    if CREDENTIAL_PATH:
        genai.configure(api_key=CREDENTIAL_PATH)


def get_generative_model(model_family: str = None) -> genai.GenerativeModel:
    """
    Return a configured Vertex AI generative model instance.

    Args:
        model_family (str): Optional specific model identifier (e.g., 'gemini-1.5-flash').

    Returns:
        genai.GenerativeModel: Ready-to-use model instance.
    """
    model_family = model_family or DEFAULT_MODEL_FAMILY
    return genai.GenerativeModel(model_family)


def build_prompt(messages: list[dict]) -> str:
    """
    Helper to convert OpenAI-style message list into a plain text prompt
    for Vertex AI. This is a simple concatenation; advanced formatting can be added.

    Args:
        messages (list[dict]): List of {\"role\": ..., \"content\": ...} entries.

    Returns:
        str: Prompt string.
    """
    prompt = []
    for msg in messages:
        prompt.append(f"<{msg['role']}> {msg['content']} </{msg['role']}> ", end='')
    return "".join(prompt)

# Example usage (uncomment to test)
#if __name__ == "__main__":
#    configure_client()
#    model = get_generative_model()
#    print(model.generate_content("Hello, world!"))
