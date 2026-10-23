import os
import cohere
from security_models import TextEmbeddingRequest, TextEmbeddingResponse

def get_audit_embedding(request: TextEmbeddingRequest) -> TextEmbeddingResponse:
    """
    Generates a vector embedding for a crypto audit note using Cohere.
    
    Args:
        request: A TextEmbeddingRequest containing the text to embed.

    Returns:
        A TextEmbeddingResponse with the resulting vector embedding.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    try:
        response = co.embed(
            texts=[request.text_to_embed],
            model="embed-english-v3.0",
            input_type="search_document"
        )
        embedding = response.embeddings[0]
        return TextEmbeddingResponse(embedding=embedding)
    except Exception as e:
        print(f"An error occurred with the Cohere API: {e}")
        raise

