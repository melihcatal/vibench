import os
import cohere
from typing import List


def embed_narration_script(script_text: str) -> List[float]:
    """
    Generates embeddings for a narration script using the Cohere API.

    Requires the CO_API_KEY environment variable.

    Args:
        script_text: The narration script to embed.

    Returns:
        A list of floats representing the embedding vector.
        
    Raises:
        ValueError: If the CO_API_KEY is not set.
    """
    api_key = os.getenv("CO_API_KEY")
    if not api_key:
        raise ValueError("CO_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    try:
        response = co.embed(
            texts=[script_text],
            model="embed-english-v3.0",
            input_type="search_document"
        )
        return response.embeddings[0]
    except cohere.errors.CohereError as e:
        print(f"Cohere API error: {e}")
        raise
    except (IndexError, TypeError) as e:
        print(f"Failed to parse Cohere API response: {e}")
        raise
