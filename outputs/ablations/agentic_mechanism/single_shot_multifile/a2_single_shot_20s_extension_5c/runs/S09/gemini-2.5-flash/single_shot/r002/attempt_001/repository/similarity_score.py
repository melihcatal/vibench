import os
from typing import List
import numpy as np

import vertexai
from vertexai.preview.language_models import TextEmbeddingModel

def _get_vertex_embedding(text: str) -> List[float]:
    vertexai.init(project=os.environ.get("GOOGLE_CLOUD_PROJECT"), location=os.environ.get("GOOGLE_CLOUD_LOCATION"))
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    embeddings = model.get_embeddings([text])
    return embeddings[0].values

def cosine_similarity(text1: str, text2: str) -> float:
    embedding1 = _get_vertex_embedding(text1)
    embedding2 = _get_vertex_embedding(text2)

    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)

    dot_product = np.dot(vec1, vec2)
    norm_a = np.linalg.norm(vec1)
    norm_b = np.linalg.norm(vec2)

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)