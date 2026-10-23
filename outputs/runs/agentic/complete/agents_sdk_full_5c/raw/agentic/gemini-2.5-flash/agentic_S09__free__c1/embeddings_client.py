from google.cloud import aiplatform
from google.cloud.aiplatform.models import TextEmbeddingModel

def get_vertex_embeddings_model(project_id: str, location: str, model_name: str = "textembedding-gecko@003") -> TextEmbeddingModel:
    """Provides a configured Vertex AI TextEmbeddingModel client.

    Args:
        project_id: Your Google Cloud project ID.
        location: The region for the Vertex AI endpoint (e.g., "us-central1").
        model_name: The name of the embedding model (default: "textembedding-gecko@003").

    Returns:
        An initialized Vertex AI TextEmbeddingModel client.
    """
    aiplatform.init(project=project_id, location=location)
    model = TextEmbeddingModel.from_pretrained(model_name)
    return model

if __name__ == '__main__':
    # Example usage:
    # from google.cloud.aiplatform.gapic.schema.predict.prediction.text_embedding import TextEmbedding
    # project_id = "YOUR_PROJECT_ID"
    # location = "us-central1"
    # client = get_vertex_embeddings_model(project_id, location)
    # print(f"Successfully initialized Vertex AI embedding model: {client._model_id}")
    # # You can then use the client to get embeddings:
    # # embeddings = client.get_embeddings(["test text"])
    # # print(embeddings[0].values)
    pass
