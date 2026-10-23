import os
from typing import List
import google.generativeai as genai

def embed_text(text: str) -> List[float]:
    """
    Embeds a given text using Google's PaLM API for semantic search.

    Args:
        text: The text to embed.

    Returns:
        A list of floats representing the embedding vector.

    Raises:
        ValueError: If GOOGLE_API_KEY environment variable is not set.
        RuntimeError: For errors during the API call.
    """
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("Environment variable GOOGLE_API_KEY not set.")

    genai.configure(api_key=google_api_key)

    try:
        # Using a suitable embedding model, e.g., 'text-embedding-004'
        # The exact model name might vary or be updated, so choosing a generic one
        # or specifying based on the latest available. For this example, assuming
        # a common embedding model provided by the API.
        # If a specific model like `embedding-001` or `text-embedding-004` is available, use that.
        # For now, using a placeholder for the model name.
        model = genai.GenerativeModel('embedding-001') # This is an example, use actual model ID
        response = model.embed_content(content=text, task_type="SEMANTIC_SIMILARITY")
        return response['embedding']
    except Exception as e:
        raise RuntimeError(f"Error embedding text with Google PaLM API: {e}")

def embed_secret_audit_notes(audit_notes: str) -> List[float]:
    """
    Embeds secret audit notes for semantic search.

    Args:
        audit_notes: The audit notes text.

    Returns:
        A list of floats representing the embedding vector of the notes.
    """
    return embed_text(audit_notes)
