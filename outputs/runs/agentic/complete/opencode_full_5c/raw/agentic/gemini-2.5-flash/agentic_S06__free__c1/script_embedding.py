import vertexai
from vertexai.language_models import TextEmbeddingModel
import os


def get_text_embedding(
    text: str, project_id: str, location: str = "us-central1"
) -> list[float]:
    vertexai.init(project=project_id, location=location)
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
    embeddings = model.get_embeddings([text])
    return embeddings[0].values
