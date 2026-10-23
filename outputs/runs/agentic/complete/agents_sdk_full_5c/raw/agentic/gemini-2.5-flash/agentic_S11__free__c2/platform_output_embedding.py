import vertexai
from vertexai.language_models import TextEmbeddingModel

def platform_output_embedding(project_id: str, location: str, model_name: str, text: str):
    """Embeds platform outputs for evaluation or retrieval using Vertex AI Embedding Model."""
    vertexai.init(project=project_id, location=location)
    model = TextEmbeddingModel.from_pretrained(model_name)

    # The input to embed_text can be a list of strings
    response = model.embed_text(text=[text])

    # Extract the embedding values
    embeddings = [embedding.values for embedding in response.embeddings]

    return {
        "text": text,
        "embedding": embeddings[0] if embeddings else [],
        "model_name": model_name
    }
