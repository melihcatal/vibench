from safety_client import get_cohere_client
from safety_models import EmbeddingRequest, EmbeddingResponse

def moderation_reason_embedding(request: EmbeddingRequest) -> EmbeddingResponse:
    """
    Generates an embedding for a moderation rationale using the Cohere API.
    
    This can be used for finding similar past cases or for classification.

    Args:
        request: An EmbeddingRequest containing the text to embed.

    Returns:
        An EmbeddingResponse with the original text and its vector embedding.
    """
    client = get_cohere_client()
    
    response = client.embed(
        texts=[request.text],
        model='embed-english-v3.0',
        input_type='search_document' # Use 'search_document' for storing and retrieving
    )
    
    embedding = response.embeddings[0]
    
    return EmbeddingResponse(
        text=request.text,
        embedding=embedding
    )
