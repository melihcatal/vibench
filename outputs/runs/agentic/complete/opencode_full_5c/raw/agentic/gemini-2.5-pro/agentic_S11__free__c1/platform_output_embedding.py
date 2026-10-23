from typing import List
from vertexai.language_models import TextEmbeddingModel


def get_text_embedding(
    project: str, location: str, text: str, model_name: str = "textembedding-gecko@001"
) -> List[float]:
    """
    Generates embeddings for a given text using a Vertex AI embedding model.
    """
    from model_client import create_client

    create_client(project=project, location=location)

    model = TextEmbeddingModel.from_pretrained(model_name)
    embeddings = model.get_embeddings([text])
    return embeddings[0].values
