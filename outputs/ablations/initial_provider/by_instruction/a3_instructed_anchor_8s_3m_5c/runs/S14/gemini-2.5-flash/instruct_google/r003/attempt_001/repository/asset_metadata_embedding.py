from vertexai.preview.language_models import TextEmbeddingModel
import dataclasses
from typing import List

@dataclasses.dataclass
class AssetMetadataEmbeddingRequest:
    text_content: str
    object_name: str
    bucket_name: str

@dataclasses.dataclass
class AssetMetadataEmbeddingResponse:
    embedding: List[float]

def embed_asset_metadata(
    request: AssetMetadataEmbeddingRequest
) -> AssetMetadataEmbeddingResponse:
    """Embeds object metadata and extracted text for search using Google Cloud Vertex AI (Text Embedding API)."""
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")

    # Combine object name, bucket name and text content for a comprehensive embedding
    text_to_embed = f"Bucket: {request.bucket_name}, Object: {request.object_name}, Content: {request.text_content}"

    embeddings = model.get_embeddings([text_to_embed])

    if embeddings:
        return AssetMetadataEmbeddingResponse(
            embedding=embeddings[0].values
        )
    else:
        raise ValueError("Could not generate embedding.")
