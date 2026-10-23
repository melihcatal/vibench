import vertexai
from vertexai.preview.language_models import TextEmbeddingModel
from typing import List

def asset_metadata_embedding(text_to_embed: List[str], project_id: str, location: str = "us-central1") -> List[List[float]]:
    """
    Embeds text content using Google Cloud Vertex AI Text Embedding API.
    """
    vertexai.init(project=project_id, location=location)
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")

    embeddings = model.get_embeddings(text_to_embed)
    
    return [embedding.values for embedding in embeddings]
