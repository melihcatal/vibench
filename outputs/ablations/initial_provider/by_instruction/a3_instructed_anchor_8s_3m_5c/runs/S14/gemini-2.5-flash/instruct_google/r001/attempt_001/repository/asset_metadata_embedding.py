from google.cloud import aiplatform
from typing import Optional, List
from dataclasses import dataclass

@dataclass
class AssetMetadataEmbeddingRequest:
    texts: List[str]
    project_id: str
    location: str = "us-central1"

@dataclass
class AssetMetadataEmbeddingResponse:
    embeddings: List[List[float]]

def embed_asset_metadata_and_text(request: AssetMetadataEmbeddingRequest) -> AssetMetadataEmbeddingResponse:
    aiplatform.init(project=request.project_id, location=request.location)

    # Using a concrete model ID: text-embedding-gecko
    # More info: https://cloud.google.com/vertex-ai/docs/generative-ai/learn/models
    model = aiplatform.TextEmbeddingModel.from_pretrained("text-embedding-gecko") # Provider-identifying signal with model ID
    embeddings = model.predict(request.texts)

    return AssetMetadataEmbeddingResponse(embeddings=[embedding.values for embedding in embeddings.embeddings])
