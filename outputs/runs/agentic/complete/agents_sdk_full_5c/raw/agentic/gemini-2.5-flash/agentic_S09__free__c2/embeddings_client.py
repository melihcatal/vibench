from google.cloud import aiplatform

def get_vertex_ai_embedding_model(project_id: str, location: str, model_name: str = "textembedding-gecko@003") -> aiplatform.TextEmbeddingModel:
    """Initializes and returns a Vertex AI TextEmbeddingModel client.

    Args:
        project_id: Your Google Cloud project ID.
        location: The region for the Vertex AI endpoint (e.g., "us-central1").
        model_name: The name of the embedding model to use (default: "textembedding-gecko@003").

    Returns:
        An initialized Vertex AI TextEmbeddingModel instance.
    """
    aiplatform.init(project=project_id, location=location)
    return aiplatform.TextEmbeddingModel.from_pretrained(model_name)

if __name__ == '__main__':
    # Example usage:
    # from google.cloud.aiplatform_v1beta1.types import Embedding
    # model = get_vertex_ai_embedding_model(project_id="your-project-id", location="us-central1")
    # embeddings_response = model.get_embeddings(texts=["Hello from the client helper!"])
    # for embedding in embeddings_response:
    #     print(f"Embedding values count: {len(embedding.values)}")
    pass
