import os
import json
from typing import Dict, Any

import openai
from storage_models import EmbeddingVector

def create_embedding_for_asset(
    metadata: Dict[str, Any], extracted_text: str
) -> EmbeddingVector:
    """
    Creates a vector embedding for an asset using its metadata and text content
    with the OpenAI API.

    Requires the OPENAI_API_KEY environment variable.

    :param metadata: A dictionary of asset metadata.
    :param extracted_text: The text content extracted from the asset.
    :return: An EmbeddingVector object.
    """
    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable not set.")
        
    client = openai.OpenAI()

    # Combine metadata and text into a single string for embedding
    # Using JSON for a structured representation of metadata
    metadata_str = json.dumps(metadata, sort_keys=True)
    combined_input = f"Metadata: {metadata_str}\n\nContent:\n{extracted_text}"

    model_id = "text-embedding-3-small"

    try:
        response = client.embeddings.create(
            input=[combined_input], 
            model=model_id
        )

        embedding_data = response.data[0]
        usage = response.usage

        return EmbeddingVector(
            model=model_id,
            vector=embedding_data.embedding,
            total_tokens=usage.total_tokens
        )
    except openai.APIError as e:
        print(f"OpenAI API error: {e}")
        raise
