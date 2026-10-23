import os
from typing import List, Dict, Union
import google.generativeai as genai


def get_embedding_for_text(text_to_embed: Union[str, List[str]]) -> List[List[float]]:
    """
    Generates embeddings for a given text or list of texts using Gemini API.

    Args:
        text_to_embed: A string or a list of strings to embed.

    Returns:
        A list of embeddings, where each embedding is a list of floats.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = "models/embedding-001"

    if isinstance(text_to_embed, str):
        text_to_embed = [text_to_embed]

    result = genai.embed_content(
        model=model, content=text_to_embed, task_type="retrieval_document"
    )

    return result["embedding"]


def embed_asset_metadata(metadata: Dict[str, str], extracted_text: str) -> List[float]:
    """
    Combines asset metadata and extracted text into a single string
    and generates an embedding for it.

    Args:
        metadata: A dictionary of asset metadata.
        extracted_text: Text extracted from the asset.

    Returns:
        A list of floats representing the embedding.
    """
    combined_text = " ".join([f"{k}: {v}" for k, v in metadata.items()])
    full_text = f"{combined_text}\n\nContent:\n{extracted_text}"

    embedding = get_embedding_for_text(full_text)
    return embedding[0]
