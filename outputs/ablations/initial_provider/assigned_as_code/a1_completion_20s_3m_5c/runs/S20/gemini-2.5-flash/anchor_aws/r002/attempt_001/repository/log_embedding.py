from typing import List, Dict, Any
from observability_client import ObservabilityClient
from observability_models import EmbeddingRequest

def embed_log_messages(text_content: List[str], project_id: str, location: str) -> Dict[str, Any]:
    client = ObservabilityClient(region_name="us-east-1", project_id=project_id, location=location)
    model = client.get_text_embedding_model("text-embedding-gecko@003") # Using a specific embedding model

    response = model.embed_text(text_content)

    embeddings = []
    for embedding in response.embeddings:
        embeddings.append(embedding.values)

    return {"text_content": text_content, "embeddings": embeddings}
