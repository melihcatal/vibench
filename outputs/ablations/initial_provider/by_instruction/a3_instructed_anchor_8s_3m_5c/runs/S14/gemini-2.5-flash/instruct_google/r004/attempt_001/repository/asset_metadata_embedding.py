from google.cloud import aiplatform
from google.protobuf import struct_pb2

from storage_client import get_aiplatform_text_embedding_client
from storage_models import AssetMetadataEmbeddingRequest, AssetMetadataEmbeddingResponse

def embed_asset_metadata(
    request: AssetMetadataEmbeddingRequest
) -> AssetMetadataEmbeddingResponse:
    """Embeds object metadata and extracted text for search using Google Cloud AI Platform (Vertex AI)."""
    # aiplatform.init ensures project and location are set for Vertex AI operations.
    # These should ideally come from environment variables or a configuration file.
    aiplatform.init(project=request.project_id, location=request.location)
    
    # For embedding models like text-embedding-004, you can directly use the EmbeddingModel class.
    # The model ID should be specified, e.g., "text-embedding-004".
    model = aiplatform.language_models.TextEmbeddingModel.from_pretrained(request.model_name)

    # The embed method takes a list of texts to embed.
    embeddings = model.get_embeddings([request.content])

    # The embedding result is a list of Embedding objects, each containing a list of floats.
    # We extract the first embedding's values.
    embedding_values = embeddings[0].values

    return AssetMetadataEmbeddingResponse(
        embedding=embedding_values,
    )
