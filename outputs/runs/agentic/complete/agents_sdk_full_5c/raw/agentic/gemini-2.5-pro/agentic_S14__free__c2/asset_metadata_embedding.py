import cohere
import json
from typing import Dict, Any, List
from storage_models import EmbeddingResult

def create_metadata_and_text_embedding(
    metadata: Dict[str, Any],
    extracted_text: str,
    input_type: str = "search_document"
) -> EmbeddingResult:
    """
    Creates embeddings for object metadata and extracted text using Cohere.

    :param metadata: A dictionary of object metadata.
    :param extracted_text: The text content extracted from the object.
    :param input_type: The type of input for the Cohere API ('search_document' or 'search_query').
    :return: An EmbeddingResult object.
    """
    # Assumes COHERE_API_KEY environment variable is set
    co = cohere.Client()
    
    model_name = "embed-english-v3.0"
    
    # Combine metadata and text into a single structured string
    # JSON serialization is a simple way to represent the metadata dictionary
    metadata_str = json.dumps(metadata, sort_keys=True)
    combined_text = f"Metadata: {metadata_str}\n\nContent: {extracted_text}"

    texts_to_embed = [combined_text]

    response = co.embed(
        texts=texts_to_embed,
        model=model_name,
        input_type=input_type
    )

    return EmbeddingResult(
        texts=texts_to_embed,
        embeddings=response.embeddings,
        model_used=model_name
    )
