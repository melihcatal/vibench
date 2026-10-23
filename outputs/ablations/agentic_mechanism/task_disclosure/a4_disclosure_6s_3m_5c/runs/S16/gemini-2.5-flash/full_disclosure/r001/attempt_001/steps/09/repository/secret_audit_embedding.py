import vertexai
from vertexai.preview.language_models import TextEmbeddingModel

def embed_audit_notes(text: str) -> list[float]:
    """
    Embeds secret audit notes for semantic search using Google's Vertex AI.
    """
    vertexai.init()
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko")
    embeddings = model.get_embeddings([text])
    return embeddings[0].values
