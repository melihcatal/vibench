import os
import cohere

def embed_script(script_text: str, model_name: str = "embed-english-v3.0") -> list[float]:
    """
    Generates embeddings for a narration script using the Cohere API.

    Args:
        script_text: The text of the narration script.
        model_name: The Cohere embedding model to use.

    Returns:
        A list of floats representing the embedding vector.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    response = co.embed(
        texts=[script_text],
        model=model_name,
        input_type="search_document"
    )
    
    return response.embeddings[0]
