from vertexai.language_models import TextEmbeddingModel
import vertexai

def platform_output_embedding(project_id: str, location: str, text_output: str):
    """
    Embeds platform outputs for evaluation or retrieval using Google Cloud Vertex AI Embeddings.
    """
    vertexai.init(project=project_id, location=location)
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003") # Specify the model version

    embeddings = model.get_embeddings([text_output])
    
    # Each embedding is a list of floats
    embedding_values = [embedding.values for embedding in embeddings]

    return {"embeddings": embedding_values}
