from typing import Dict, Any
from storage_client import get_cohere_client
from storage_models import AssetEmbedding


def get_asset_embedding(
    metadata: Dict[str, Any], extracted_text: str, object_name: str
) -> AssetEmbedding:
    """
    Creates an embedding for asset metadata and extracted text using Cohere.

    Args:
        metadata: A dictionary of object metadata.
        extracted_text: Text extracted from the asset.
        object_name: The name of the source asset object.

    Returns:
        An AssetEmbedding object.
    """
    cohere_client = get_cohere_client()

    metadata_str = " ".join([f"{k}:{v}" for k, v in metadata.items()])

    full_text = f"Metadata: {metadata_str}\nContent: {extracted_text}"

    model = "embed-english-v3.0"

    response = cohere_client.embed(
        texts=[full_text], model=model, input_type="search_document"
    )

    embedding = response.embeddings[0]

    return AssetEmbedding(source_object=object_name, embedding=embedding, model=model)
