from typing import List
from speech_client import cohere_client
from speech_models import EmbeddingResult

def embed_transcript_segments_cohere(segments: List[str]) -> EmbeddingResult:
    """
    Generates embeddings for a list of transcript segments using Cohere.

    Args:
        segments: A list of text strings (transcript segments).

    Returns:
        An EmbeddingResult object containing the embeddings.
    """
    model_name = "embed-english-v3.0"
    
    response = cohere_client.embed(
        texts=segments,
        model=model_name,
        input_type="search_document"
    )
    
    return EmbeddingResult(
        texts=segments,
        embeddings=response.embeddings,
        model=model_name
    )
