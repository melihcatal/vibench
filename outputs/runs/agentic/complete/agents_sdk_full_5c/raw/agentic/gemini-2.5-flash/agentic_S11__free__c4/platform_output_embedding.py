import vertexai
from vertexai.language_models import TextEmbeddingModel
from typing import List, Dict, Any

def platform_output_embedding(project_id: str, location: str, texts: List[str]) -> Dict[str, Any]:
    """Embeds platform outputs for evaluation or retrieval using Google Cloud Vertex AI Embedding model."""
    vertexai.init(project=project_id, location=location)
    model = TextEmbeddingModel.from_pretrained("text-embedding-gecko@003") # Use a concrete embedding model ID

    embeddings_response = model.get_embeddings(texts)

    embeddings = []
    for embedding in embeddings_response:
        embeddings.append(embedding.values)
    
    return {
        "original_texts": texts,
        "embeddings": embeddings
    }
