"""
Embed narration scripts for voice-asset search using the Cohere API.
"""
from typing import List
from speech_client import get_cohere_client
from speech_models import EmbeddingResponse

def embed_script_cohere(
    script_text: str,
    model: str = "embed-english-v3.0",
    input_type: str = "search_document"
) -> EmbeddingResponse:
    """
    Generates a vector embedding for a script using Cohere.

    Args:
        script_text: The text of the narration script.
        model: The Cohere embedding model to use.
        input_type: The type of input for the embedding model.

    Returns:
        An EmbeddingResponse object containing the vector.
    """
    client = get_cohere_client()

    response = client.embed(
        texts=[script_text],
        model=model,
        input_type=input_type,
    )

    embedding: List[float] = response.embeddings[0]

    return EmbeddingResponse(
        embedding=embedding,
        model=model
    )
