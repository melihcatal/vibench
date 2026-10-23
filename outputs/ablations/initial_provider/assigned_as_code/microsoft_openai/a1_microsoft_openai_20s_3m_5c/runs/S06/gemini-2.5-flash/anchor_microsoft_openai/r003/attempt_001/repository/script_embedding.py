import vertexai
from vertexai.language_models import TextEmbeddingModel
import os
from typing import List

def embed_script(text: str, project_id: str, location: str = "us-central1") -> List[float]:
    vertexai.init(project=project_id, location=location)
    model = TextEmbeddingModel.from_pretrained("text-embedding-gecko@003")
    embeddings = model.get_embeddings([text])
    return embeddings[0].values
