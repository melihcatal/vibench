import vertexai
from vertexai.language_models import TextEmbeddingModel
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass
class AssetMetadataEmbeddingRequest:
    texts: List[str]

@dataclass
class AssetMetadataEmbeddingResponse:
    embeddings: List[List[float]]
    full_response: Optional[Dict[str, Any]] = None

def embed_asset_metadata_and_text(request: AssetMetadataEmbeddingRequest) -> AssetMetadataEmbeddingResponse:
    # Initialize Vertex AI (you might want to move this to a central client helper)
    vertexai.init()
    
    model = TextEmbeddingModel.from_pretrained("text-embedding-004") # Using a concrete model identifier

    # The Vertex AI embedding model can take multiple texts in a single request
    embeddings_response = model.get_embeddings(request.texts)
    
    embeddings = [embedding.values for embedding in embeddings_response]

    return AssetMetadataEmbeddingResponse(embeddings=embeddings)
