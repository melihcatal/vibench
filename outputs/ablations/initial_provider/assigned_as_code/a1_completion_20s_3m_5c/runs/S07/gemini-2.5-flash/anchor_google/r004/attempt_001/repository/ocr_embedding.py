import google.cloud.aiplatform as aiplatform
from typing import List

def ocr_embedding(texts: List[str], project_id: str, location: str = "us-central1", model_name: str = "text-embedding-garden") -> List[List[float]]:
    # Initialize Vertex AI
    aiplatform.init(project=project_id, location=location)

    # Load the embedding model (e.g., text-embedding-garden or text-embedding-001)
    model = aiplatform.TextEmbeddingModel.from_pretrained(model_name)

    # Get embeddings for the list of texts
    embeddings = model.get_embeddings(texts)

    # Extract the actual embedding vectors
    embedding_vectors = [embedding.values for embedding in embeddings]

    return embedding_vectors
