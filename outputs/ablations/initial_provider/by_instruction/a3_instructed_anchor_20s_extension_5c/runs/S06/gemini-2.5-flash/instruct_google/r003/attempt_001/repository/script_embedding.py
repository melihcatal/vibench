from google.cloud import aiplatform

def embed_script(text: str) -> list[float]:
    """
    Embeds narration scripts for voice-asset search using Google Cloud Vertex AI Embeddings.
    """
    model = aiplatform.TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
    embeddings = model.get_embeddings([text])
    return embeddings[0].values
