import os
from typing import List, Dict, Union
import cohere

def get_cohere_embedding(metadata: Dict[str, Union[str, int]], content: str) -> List[float]:
    """
    Generates an embedding for a combination of asset metadata and content using Cohere.

    Args:
        metadata (Dict[str, Union[str, int]]): A dictionary of asset metadata.
        content (str): The text content of the asset.

    Returns:
        List[float]: The generated embedding vector.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    text_to_embed = []
    for key, value in metadata.items():
        text_to_embed.append(f"{key}: {value}")
    
    text_to_embed.append(f"content: {content}")
    
    combined_text = "\n".join(text_to_embed)

    response = co.embed(
        texts=[combined_text],
        model="embed-english-v3.0",
        input_type="search_document"
    )

    return response.embeddings[0]
