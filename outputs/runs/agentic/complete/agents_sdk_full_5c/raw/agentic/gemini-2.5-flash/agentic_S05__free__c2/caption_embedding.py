import vertexai
from vertexai.language_models import TextEmbeddingModel

def embed_caption_chunk(text_chunk: str, project_id: str, location: str = "us-central1"):
    """
    Generates embeddings for a caption chunk using Google Cloud Vertex AI's Text Embedding.
    """
    vertexai.init(project=project_id, location=location)
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001") # Concrete model identifier

    embeddings = model.get_embeddings([text_chunk])
    
    # Each input text generates one embedding.
    # The embedding vector is in embeddings[0].values
    return embeddings[0].values
